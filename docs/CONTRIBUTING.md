# Contributing to infoblox.universal_ddi collection

Welcome to the Universal DDI Ansible Repository! We are excited that you are interested in contributing to our project. This document outlines the process for contributing to the repository and how you can make submissions that add value and are in harmony with the current structure.

## Workflow Summary

1. [Clone the repository](#cloning)
2. [Make the desired Code Change](#writing-new-code)
3. [Run integration tests locally and ensure that they pass](#writing-integration-tests)
4. [Create a PR](#pr-creation)

## Cloning

The `ansible-test` command expects that the repository is in a directory that matches it's collection,
under a directory `ansible_collections`. Clone ensuring that hierarchy:

```shell
mkdir -p $TARGET_DIR/ansible_collections/infoblox
git clone <url> $TARGET_DIR/ansible_collections/infoblox/universal_ddi
```

The python requirements must be installed separately. It is recommended to use a venv to keep the dependencies local. 
Set up your Python virtual environment

```shell
cd $TARGET_DIR/ansible_collections/infoblox/universal_ddi
python3 -m venv .venv
source .venv/bin/activate
pip3 install ansible
pip3 install -r requirements.txt
```

You can run ```ansible-test sanity``` to test if your collection is ready for development

## Writing New Code

### Writing New Modules
 
Create two files for each module:
- `module_name.py`: The main module code.
- `module_name_info.py`: For gathering module resource information.

Place these files under `/plugins/modules`.

#### Documentation Examples and Return section inside modules

**Documentation Section** Each module file should start with a comprehensive documentation section. [Module format and documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#module-format-and-documentation) guide gives  details about how to document.

**Examples Section** Provides practical usage examples demonstrating standard and edge case scenarios.

**Return Section** Clearly document what values the module returns.

### Writing Integration Tests

- All modules MUST have integration tests for new features. Bug fixes for modules that currently have integration tests SHOULD have tests added.

- Start by adding tests in tests/integration/targets/MODULE_NAME for your new feature.

- Each module must also be added to the all group in meta/runtime.yml. This will allow to reuse common variables like portal_key in the test. 


#### Expected test criteria:
- Resource creation under check mode
- Resource creation
- Resource creation again (idempotency)
- Resource deletion under check mode
- Resource deletion
- Resource deletion again (idempotency)
- Resource creation with additional parameters
- Resource modification

#### Running Tests Locally

For local testing, ensure you set up your integration test configuration
1. Navigate to `tests/integration` folder
2. Create or update the integration_config.yaml file with necessary environment-specific configurations such as
   ```shell
   portal_url: https://csp.infoblox.com
   portal_key: "your-portal-secret-key"
   ```
   - The default URL for the Cloud Services Portal is https://csp.infoblox.com
   - An API key is required to access Infoblox API. You can obtain an API key by following the instructions in the guide for [Configuring User API Keys](https://docs.infoblox.com/space/BloxOneCloud/35430405/Configuring+User+API+Keys).


Run tests for the desired module(s):

```shell
ansible-test integration <module_name> 
```
If you want more detailed output, run the command with -vvv 

```shell
ansible-test integration <module_name> -vvv
```

## PR Creation

- Before raising your PR, you must make sure the PR is merge worthy.
- The PR will trigger some check actions in Github. The PR can be only merged when these tests pass. You can also test your PR locally with these commands. 

```shell
ansible-test sanity
```

```shell
ansible-test integration
```

## Reporting an issue

- When you find a bug, you can help tremendously by reporting an issue.
- Please [search in the issue list](https://github.com/infobloxopen/universal-ddi-ansible/issues) and if it has not been already reported, [open a new issue](https://github.com/infobloxopen/universal-ddi-ansible/issues/new)
- If you discover that the bug you're trying to file already exists in an issue, you can help by verifying the behavior of the reported bug with a comment in that issue, or by reporting any additional information

## More information about contributing

- General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).

- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly
 
- `infoblox.universal_ddi` modules uses the Universal DDI Python client library. This provides a more consistent experience across the modules and supports a wider range of BloxOne services.
Information about its usage can be found [here](https://github.com/infobloxopen/universal-ddi-python-client/blob/main/README.md)

## Code of Conduct 

The `infoblox.universal_ddi` collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.