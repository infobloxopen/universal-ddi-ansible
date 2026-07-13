"""
Integration test cleanup script.

Deletes resources whose names start with one of the configured prefixes.
Each resource type has its own default prefixes (see default_prefixes on each class).
Reads credentials from integration_config.yml, environment variables, or CLI flags.

Usage:
    python cleanup.py                              # dry-run preview (uses per-cleaner defaults)
    python cleanup.py --delete                     # actually delete
    python cleanup.py --delete --prefixes my-test  # override prefixes for ALL resource types
    python cleanup.py --delete --only "DNS Views"  # single resource type
"""

from __future__ import annotations

import argparse
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

import universal_ddi_client
from universal_ddi_client import ApiException
from dns_config import AclApi, AuthNsgApi, AuthZoneApi, ForwardNsgApi, ForwardZoneApi, ServerApi, ViewApi
from infra_mgmt import DetailApi, HostsApi, ServicesApi
from ipam import IpSpaceApi, OptionGroupApi, OptionSpaceApi
from ipam_federation import FederatedRealmApi

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG_PATH = _SCRIPT_DIR / "integration_config.yml"
_PAGE_SIZE = 500


# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

def _build_client(portal_url: str, portal_key: str) -> universal_ddi_client.ApiClient:
    config = universal_ddi_client.Configuration(
        portal_url=portal_url,
        portal_key=portal_key,
        client_name="cleanup-script",
    )
    return universal_ddi_client.ApiClient(config)


def _load_yaml_config(path: Path) -> dict:
    """Parse a simple flat YAML config (key: value lines, no nesting)."""
    result = {}
    if not path.is_file():
        return result
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


# ---------------------------------------------------------------------------
# Pagination helper
# ---------------------------------------------------------------------------

def _paginate(api_list_fn, **kwargs) -> Iterator:
    """
    Yield every result from a paginated list call.

    Passes **kwargs through to the API function on every page.
    Stops when a page returns fewer items than _PAGE_SIZE (last page).
    """
    offset = 0
    while True:
        resp = api_list_fn(limit=_PAGE_SIZE, offset=offset, **kwargs)
        results = resp.results or []
        yield from results
        if len(results) < _PAGE_SIZE:
            break
        offset += _PAGE_SIZE


# ---------------------------------------------------------------------------
# Base cleaner
# ---------------------------------------------------------------------------

class ResourceCleaner(ABC):
    """
    Base class for a single resource type.

    Subclass contract:
        resource_name    – human-readable label shown in output (e.g. "IP Spaces")
        default_prefixes – name prefixes this cleaner targets when no global
                           override is passed on the CLI
        list_all()       – return an iterable of objects each having .id and .name
        delete(id)       – delete the resource with the given ID
    """

    resource_name: str = "Unknown Resource"
    default_prefixes: tuple[str, ...] = ()

    def __init__(self, client: universal_ddi_client.ApiClient) -> None:
        self.client = client

    @abstractmethod
    def list_all(self):
        """Return an iterable of resource objects with .id and a name attribute."""

    @abstractmethod
    def delete(self, resource_id: str) -> None:
        """Delete the resource identified by resource_id."""

    def get_name(self, resource) -> str | None:
        """Extract the display name from a resource object.

        Override when the model uses a field other than .name (e.g. display_name).
        """
        return resource.name

    # ------------------------------------------------------------------
    # Orchestration — not normally overridden
    # ------------------------------------------------------------------

    def cleanup(
        self,
        prefixes: tuple[str, ...],
        *,
        dry_run: bool,
    ) -> tuple[int, int]:
        """
        Delete all resources whose names start with any of *prefixes*.

        Returns (deleted_count, error_count).
        dry_run=True prints what would be deleted without touching anything.
        """
        print(f"\n{'[DRY RUN] ' if dry_run else ''}=== {self.resource_name} ===")

        try:
            candidates = [
                r for r in self.list_all()
                if self.get_name(r) and self.get_name(r).startswith(prefixes)
            ]
        except ApiException as exc:
            print(f"  ERROR listing resources: {exc}")
            return 0, 1

        if not candidates:
            print(f"  Nothing to clean up (no names matching prefixes: {prefixes})")
            return 0, 0

        deleted = errors = 0
        for resource in candidates:
            label = f"{self.get_name(resource)!r}  (id={resource.id})"
            if dry_run:
                print(f"  Would delete: {label}")
                deleted += 1
            else:
                try:
                    self.delete(resource.id)
                    print(f"  Deleted: {label}")
                    deleted += 1
                except ApiException as exc:
                    print(f"  ERROR deleting {label}: {exc}")
                    errors += 1

        return deleted, errors


# ---------------------------------------------------------------------------
# Concrete cleaners
# ---------------------------------------------------------------------------

_ZONE_REFERENCED_ERROR = "'Zone' object is referenced by a 'View'"


class DnsViewCleaner(ResourceCleaner):
    """Cleans up DNS Views, including dependent zones when necessary."""

    resource_name = "DNS Views"
    default_prefixes = ("my-test-view", "view-")

    def list_all(self):
        return _paginate(ViewApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        try:
            ViewApi(self.client).delete(resource_id)
        except ApiException as exc:
            if _ZONE_REFERENCED_ERROR not in (exc.body or ""):
                raise
            self._delete_zones_for_view(resource_id)
            ViewApi(self.client).delete(resource_id)  # retry after zones are gone

    def _delete_zones_for_view(self, view_id: str) -> None:
        view_filter = f"view=='{view_id}'"
        for zone in _paginate(AuthZoneApi(self.client).list, filter=view_filter):
            print(f"    Deleting auth zone: {zone.fqdn}  (id={zone.id})")
            AuthZoneApi(self.client).delete(zone.id)
        for zone in _paginate(ForwardZoneApi(self.client).list, filter=view_filter):
            print(f"    Deleting forward zone: {zone.fqdn}  (id={zone.id})")
            ForwardZoneApi(self.client).delete(zone.id)


class AclCleaner(ResourceCleaner):
    """Cleans up DNS ACLs."""

    resource_name = "ACLs"
    default_prefixes = ("acl-",)

    def list_all(self):
        return _paginate(AclApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        AclApi(self.client).delete(resource_id)


class AuthNsgCleaner(ResourceCleaner):
    """Cleans up DNS Auth NSGs."""

    resource_name = "Auth NSGs"
    default_prefixes = ("test-auth-nsg",)

    def list_all(self):
        return _paginate(AuthNsgApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        AuthNsgApi(self.client).delete(resource_id)


class ForwardNsgCleaner(ResourceCleaner):
    """Cleans up DNS Forward NSGs."""

    resource_name = "Forward NSGs"
    default_prefixes = ("test-forward-nsg",)

    def list_all(self):
        return _paginate(ForwardNsgApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        ForwardNsgApi(self.client).delete(resource_id)


class AuthZoneCleaner(ResourceCleaner):
    """Cleans up auth zones in the default DNS view."""

    resource_name = "Auth Zones (default view)"
    default_prefixes = ("zone-", "tf-acc-test", "auth-zone-")

    def list_all(self):
        views = list(_paginate(ViewApi(self.client).list, filter="name=='default'"))
        if not views:
            return []
        return _paginate(AuthZoneApi(self.client).list, filter=f"view=='{views[0].id}'")

    def get_name(self, resource) -> str | None:
        return resource.fqdn

    def delete(self, resource_id: str) -> None:
        AuthZoneApi(self.client).delete(resource_id)


class DnsServerCleaner(ResourceCleaner):
    """Cleans up DNS Servers."""

    resource_name = "DNS Servers"
    default_prefixes = ("dns-server",)

    def list_all(self):
        return _paginate(ServerApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        ServerApi(self.client).delete(resource_id)


class OptionSpaceCleaner(ResourceCleaner):
    """Cleans up IPAM Option Spaces."""

    resource_name = "Option Spaces"
    default_prefixes = ("test-option-space",)

    def list_all(self):
        return _paginate(OptionSpaceApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        OptionSpaceApi(self.client).delete(resource_id)


class OptionGroupCleaner(ResourceCleaner):
    """Cleans up IPAM Option Groups."""

    resource_name = "Option Groups"
    default_prefixes = ("option-code",)

    def list_all(self):
        return _paginate(OptionGroupApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        OptionGroupApi(self.client).delete(resource_id)


class FederatedRealmCleaner(ResourceCleaner):
    """Cleans up IPAM Federation Federated Realms."""

    resource_name = "Federated Realms"
    default_prefixes = ("test-federated-realm-",)

    def list_all(self):
        return _paginate(FederatedRealmApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        FederatedRealmApi(self.client).delete(resource_id)


class IpSpaceCleaner(ResourceCleaner):
    """Cleans up IPAM IP Spaces."""

    resource_name = "IP Spaces"
    default_prefixes = ("ip-space", "test")

    def list_all(self):
        return _paginate(IpSpaceApi(self.client).list)

    def delete(self, resource_id: str) -> None:
        IpSpaceApi(self.client).delete(resource_id)


_SERVICE_HOST_NAMES = {"TF_TEST_HOST_01", "TF_TEST_HOST_02", "TF_TEST_HOST_03", "TF_TEST_HOST_04"}


class DetailServicesCleaner(ResourceCleaner):
    """
    Cleans up anycast services where:
      - hosts[0].composite_status is not 'online'
      - hosts[0].display_name is one of the known test hosts
    Filtering is by service criteria, not by name prefix.
    """

    resource_name = "Detail Services"

    def list_all(self):
        return _paginate(DetailApi(self.client).services_list, filter="service_type=='anycast'")

    def delete(self, resource_id: str) -> None:
        ServicesApi(self.client).delete(resource_id)

    def cleanup(self, prefixes: tuple[str, ...], *, dry_run: bool) -> tuple[int, int]:
        print(f"\n{'[DRY RUN] ' if dry_run else ''}=== {self.resource_name} ===")

        try:
            candidates = [
                svc for svc in self.list_all()
                if svc.hosts
                and svc.hosts[0].composite_status != "online"
                and svc.hosts[0].display_name in _SERVICE_HOST_NAMES
            ]
        except ApiException as exc:
            print(f"  ERROR listing resources: {exc}")
            return 0, 1

        if not candidates:
            print("Nothing to clean up")
            return 0, 0

        deleted = errors = 0
        for svc in candidates:
            label = (
                f"{svc.name!r}  (id={svc.id}, "
                f"host={svc.hosts[0].display_name}, "
                f"status={svc.hosts[0].composite_status})"
            )
            if dry_run:
                print(f"  Would delete: {label}")
                deleted += 1
            else:
                try:
                    self.delete(svc.id)
                    print(f"  Deleted: {label}")
                    deleted += 1
                except ApiException as exc:
                    print(f"  ERROR deleting {label}: {exc}")
                    errors += 1

        return deleted, errors


class HostsCleaner(ResourceCleaner):
    """Cleans up hosts with composite_status=='pending' via DetailApi/HostsApi."""

    resource_name = "Hosts"
    default_prefixes = ("host-", "test-host")

    def list_all(self):
        return _paginate(DetailApi(self.client).hosts_list, filter="composite_status=='pending'")

    def get_name(self, resource) -> str | None:
        return resource.display_name

    def delete(self, resource_id: str) -> None:
        HostsApi(self.client).delete(resource_id)


# ---------------------------------------------------------------------------
# Registry — order here controls deletion order.
# Add new ResourceCleaner subclasses and insert at the right position.
# ---------------------------------------------------------------------------

CLEANERS: list[type[ResourceCleaner]] = [
    DetailServicesCleaner,
    HostsCleaner,
    AclCleaner,
    AuthNsgCleaner,
    ForwardNsgCleaner,
    AuthZoneCleaner,
    DnsServerCleaner,
    DnsViewCleaner,
    OptionSpaceCleaner,
    OptionGroupCleaner,
    FederatedRealmCleaner,
    IpSpaceCleaner,
    # Example — uncomment and import the relevant API to enable:
    # AddressBlockCleaner,
    # SubnetCleaner,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(
    portal_url: str,
    portal_key: str,
    *,
    prefix_override: tuple[str, ...] | None = None,
    dry_run: bool,
    only: list[str] | None = None,
) -> bool:
    """
    Run cleanup for all registered cleaners (or the subset named in *only*).

    prefix_override: when set, all cleaners use this instead of their own
                     default_prefixes. When None, each cleaner uses its own.
    Returns True if there were no errors.
    """
    client = _build_client(portal_url, portal_key)
    only_lower = {n.lower() for n in only} if only else None

    total_deleted = total_errors = 0
    for cleaner_cls in CLEANERS:
        if only_lower and cleaner_cls.resource_name.lower() not in only_lower:
            continue
        prefixes = prefix_override if prefix_override is not None else cleaner_cls.default_prefixes
        deleted, errors = cleaner_cls(client).cleanup(prefixes, dry_run=dry_run)
        total_deleted += deleted
        total_errors += errors

    print(f"\n{'─' * 50}")
    print(f"Total: {total_deleted} {'would be ' if dry_run else ''}deleted, {total_errors} error(s)")
    return total_errors == 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Delete integration-test resources by name prefix.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--delete",
        action="store_true",
        default=False,
        help="Actually delete resources (default is dry-run / preview only).",
    )
    p.add_argument(
        "--prefixes",
        nargs="+",
        default=None,
        metavar="PREFIX",
        help=(
            "Override name prefixes for ALL resource types. "
            "When omitted, each cleaner uses its own default_prefixes."
        ),
    )
    p.add_argument(
        "--only",
        nargs="+",
        metavar="RESOURCE_NAME",
        help='Restrict cleanup to specific resource types, e.g. "IP Spaces".',
    )
    p.add_argument(
        "--portal-url",
        metavar="URL",
        help="Infoblox portal URL (overrides config file / INFOBLOX_PORTAL_URL).",
    )
    p.add_argument(
        "--portal-key",
        metavar="KEY",
        help="Infoblox API key (overrides config file / INFOBLOX_PORTAL_KEY).",
    )
    p.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        metavar="FILE",
        help=f"Path to integration_config.yml (default: {DEFAULT_CONFIG_PATH}).",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    # Credential resolution order: CLI > env var > config file
    cfg = _load_yaml_config(Path(args.config))
    portal_url = (
        args.portal_url
        or os.environ.get("INFOBLOX_PORTAL_URL")
        or cfg.get("portal_url")
    )
    portal_key = (
        args.portal_key
        or os.environ.get("INFOBLOX_PORTAL_KEY")
        or cfg.get("portal_key")
    )

    if not portal_url or not portal_key:
        sys.exit(
            "ERROR: portal_url and portal_key are required.\n"
            "  Supply them via --portal-url/--portal-key, "
            "INFOBLOX_PORTAL_URL/INFOBLOX_PORTAL_KEY env vars, "
            f"or {DEFAULT_CONFIG_PATH}."
        )

    prefix_override = tuple(args.prefixes) if args.prefixes else None
    dry_run = not args.delete

    if dry_run:
        print("DRY RUN — pass --delete to actually remove resources.")

    print(f"Portal URL : {portal_url}")
    if prefix_override:
        print(f"Prefixes   : {prefix_override}  (global override)")
    else:
        print("Prefixes   : per-cleaner defaults")
    if args.only:
        print(f"Resources  : {args.only}")

    success = run(
        portal_url,
        portal_key,
        prefix_override=prefix_override,
        dry_run=dry_run,
        only=args.only,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
