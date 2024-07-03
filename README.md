<div align="center">
    <img alt="fossunited logo" src=".github/logo.png" width="150px" height="120px">
</div>

## The FOSS United Platform

Repo for the website and open-source platform of FOSS United. The whole platform is being built on [Frappe](https://frappe.io).

## Installation

- This project works the best on the latest Frappe Version v15. And is suggested to be installed on the same.
- Checkout Frappe Framework [Installation Docs](https://frappeframework.com/docs/) for setting up frappe on your [bench](https://frappeframework.com/docs/user/en/tutorial/install-and-setup-bench).

- Create a new bench with
```bench init fossu-bench```
- Clone the FOSS United Platform App.
```bench get-app https://github.com/fossunited/fossunited```
- Create a [new site](https://frappeframework.com/docs/user/en/tutorial/create-a-site)
```bench new-site test.localhost```
- Install the App on the created site
```bench --site test.localhost install-app fossunited```
- Finally,
```bench start```

Checkout [Access site in your browser](https://frappeframework.com/docs/user/en/tutorial/create-a-site#access-site-in-your-browser) for adding hosts.

## Pre-commit

For automatic running of linters before you commit:

```
$ pip install pre-commit
$ pre-commit install
```

### Contribution

Want to contribute to the platform ? Checkout the [contribution guidelines](/docs/CONTRIBUTING.md).

### Security Policy

Please checkout [Security Policy](/docs/SECURITY.md) for information about reporting a Security Bug or Vulnerability.

## License

The repository has been released under [AGPL-3.0](https://github.com/fossunited/fossunited/blob/develop/LICENSE).
By Contributing to the FOSS United Platform, you agree that all your contributions will be licensed under AGPL License.
