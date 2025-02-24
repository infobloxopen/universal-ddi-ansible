# Contributing to infoblox.universal_ddi collection

Welcome to the Universal DDI Ansible Repository ! We're thrilled about your interest in contributing to our project. This document outlines the process for contributing to the repository and how you can make submissions that add value and are in harmony with the current structure and coding standards.
## Workflow Summary

1. [Setup](#setup)
2. [Implementing the Code Changes](#implementing-the-code-changes)
3. [Testing the Code Changes](#testing-the-code-changes)
4. [Creating a PR](#creating-a-pr)

## Setup

The `ansible-test` command expects that the repository is in a directory that matches it's collection. Here's the required directory structure you need to set up in your development environment:

```
<target_directory>/ansible_collections/infoblox/universal_ddi/
├── changelogs/
├── docs/
├── meta/
├── plugins/
│   ├── doc_fragments/
│   ├── lookup/
│   ├── module_utils/
│   ├── modules/
│   └── plugin_utils/
├── tests
│   ├── integration/
│   │   └── targets/
│   └── unit/
└── venv/
```
Before making any changes, it's essential to fork the repository. This allows you to work on your own copy of the project and makes it easy to contribute your changes back to the main repository through a pull request.

Clone the repository from GitHub ensuring the hierarchy.
```shell
mkdir -p $TARGET_DIR/ansible_collections/infoblox
git clone https://github.com/<your_username>/universal-ddi-ansible.git $TARGET_DIR/ansible_collections/infoblox/universal_ddi
```

The python requirements must be installed separately. It is recommended to use a Virtual Environment to isolate the dependencies and maintain a clean setup. 
Set up your Python virtual environment

```shell
cd $TARGET_DIR/ansible_collections/infoblox/universal_ddi
python3 -m venv .venv
source .venv/bin/activate
pip3 install ansible
pip3 install -r requirements.txt
pip3 install -r test-requirements.txt
```

You can run ```ansible-test sanity``` to test if your collection is ready for development

## Implementing the Code Changes

### Reference Documentation

Before you start contributing, it is essential to familiarize yourself with the [Infoblox API Documentation](https://csp.infoblox.com/apidoc), which provides detailed information on attributes and functionality relevant to the modules you may wish to contribute.

### Developing New Modules
 
Create two files for each module:
- `module_name.py`: Module for performing CRUD operations.
- `module_name_info.py`: Module to List / Read the object.

Place these files under `/plugins/modules`.

#### Documentation, Examples and Return section inside modules

**Documentation Section** Each module file should start with a comprehensive documentation section. [Module format and documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#module-format-and-documentation) guide gives  details about how to document.

**Examples Section** Provides practical usage examples demonstrating standard and edge case scenarios.

**Return Section** It defines what data is supposed to be returned and how it is structured.

## Testing the Code Changes

### Configuration

For local testing, ensure you set up your integration test configuration
1. Navigate to `tests/integration` folder
2. Create the integration_config.yaml file with necessary environment-specific configurations such as portal_url and portal_key as shown below.

   ```yaml
    portal_url: https://csp.infoblox.com
    portal_key: "your-portal-secret-key"
   ```
   - The default URL for the Cloud Services Portal is https://csp.infoblox.com
   - An API key is required to access Infoblox API. You can obtain an API key by following the instructions in the guide for [Configuring User API Keys](https://docs.infoblox.com/space/BloxOneCloud/35430405/Configuring+User+API+Keys).
   - These global defaults are applied to all modules in the `infoblox.universal_ddi` collection via `module_defaults`, ensuring consistent API connectivity for playbook operations:
   ```yaml
      - module_defaults:
          group/infoblox.universal_ddi.all:
            portal_url: "{{ portal_url }}"
            portal_key: "{{ portal_key }}"
   ```

### Writing Integration Tests

- Each module must also be added to the all group in meta/runtime.yml. This will allow to reuse common variables like portal_key in the test. 

- All modules MUST have integration tests for new features. Bug fixes for modules that currently have integration tests SHOULD have tests added.

- Start by adding tests in tests/integration/targets/MODULE_NAME for your new feature. The tests are supposed to be added for all writable attributes of the object. The complete list of attributes can be found in the [API Documentation](https://csp.infoblox.com/apidoc).

### Expected test criteria

- Resource creation under check mode
- Resource creation
- Resource creation again (idempotency)
- Resource deletion under check mode
- Resource deletion
- Resource deletion again (idempotency)
- Resource updation with all additional attributes under the object

For more detailed example, refer to [/tests/integration/targets/ipam_ip_space/tasks/main.yml](../tests/integration/targets/ipam_ip_space/tasks/main.yml)

### Coding Style Guidelines

-  **Properly Naming Tasks** : Each task within your tests should have a specific, descriptive name that clearly states what the test does.
      ```
    - name: "Create an IP space"
      infoblox.universal_ddi.ipam_ip_space:
          name: "{{ name }}"
          state: "present"
          .....
   ``` 

- Use well-defined and easily readable variable names.

     ```name: "test-ip-space"```

- **Clean Up After Tests**: Always clean up test artifacts to ensure tests do not interfere with each other.

    ```yaml
  always:
    # Cleanup if the test fails
    - name: "Delete IP Space"
      infoblox.universal_ddi.ipam_ip_space:
        name: "{{ name }}"
        state: "absent"
      ignore_errors: true
    ```

### Linting

To facilitate consistent coding style across the project, please run the following command before running the tests

```shell
make lint
```

The `make lint` command leverages `flynt`, `black` and `isort` ensuring proper formatting and alignment with style guidelines.

These libraries are included in `test-requirements.txt` and must be installed prior to use.

### Running Tests
Run tests for the desired module(s) using the following command

```shell
ansible-test integration <module_name> 
```

If you want more detailed output, run the command with -vvv 

```shell
ansible-test integration <module_name> -vvv
```

## Creating a PR

When you are ready to submit your Pull Request (PR), ensure it is ready for review 

- **Ensure Merge-Worthiness**: Before raising your PR, double-check that your branch is up-to-date with the main branch, conflicts are resolved, and your changes adhere to the project guidelines and quality standards.
- **Automated Tests**: Upon creating a PR, automated checks will be triggered on GitHub. These are configured to ensure that any new or modified code meets the necessary criteria for code health and functionality.

You can also test your PR locally with these commands. 

```shell
ansible-test sanity
```

```shell
ansible-test integration
```

- Your PR will be reviewed by repository maintainers. During this phase, maintainers may suggest or request changes. This feedback might relate to coding standards, functionality issues, or improvements in the logic or structure of the code.
- It is essential that you actively engage in the discussion of your PR. Respond to comments, clarify your choices when asked, and incorporate feedback appropriately.
- Once maintainers are satisfied with the updated PR and all checks are passed, the maintainer will approve the PR. 
## Reporting an issue

- When you find a bug, you can help tremendously by reporting an issue.
- Please [search in the issue list](https://github.com/infobloxopen/universal-ddi-ansible/issues) and if it has not been already reported, [open a new issue](https://github.com/infobloxopen/universal-ddi-ansible/issues/new)
- If you discover that the bug you're trying to file already exists in an issue, you can help by verifying the behavior of the reported bug with a comment in that issue, or by reporting any additional information

## More information about contributing

- General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).

- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly
 
- `infoblox.universal_ddi` modules uses the Universal DDI Python client library. This provides a more consistent experience across the modules and supports a wider range of UniversalDDI services.
Information about its usage can be found [here](https://github.com/infobloxopen/universal-ddi-python-client/blob/main/README.md)

## Code of Conduct 

The `infoblox.universal_ddi` collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.