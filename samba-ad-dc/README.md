# Samba4 AD-DC docker container

This is a docker container running Samba4 as a domain controller.

The first time you start the container, a setup-script will run and provision the domain controller using the supplied [environment variables](#environment-variables).
After the setup has finished successfully, the container will continue starting (unless `SAMBA_SETUP_ONLY` is set) and start the domain controller.

The container saves all necessary files within `/var/lib/samba`.
See the following examples on how to start/setup the domain controller and how to persist this volume.

## Examples

### Persist volume to local directory

```bash
docker run --rm -i -t \
    -e SAMBA_REALM="samba.dom" \
    -e SAMBA_PASSWORD="Password1!" \
    -e SAMBA_HOST_IP="192.168.1.10" \
    -e SAMBA_DNS_FORWARDER="192.168.1.1" \
    -v ${PWD}/samba:/var/lib/samba \
    pitkley/samba-ad-dc
```

### Persist volume using a data-container

```bash
docker run \
    --name dc_data \
    --volume /var/lib/samba \
    --entrypoint /bin/true \
    pitkley/samba-ad-dc
```

(The image used to start the data-container can be chosen arbitrarily, as long as it supplies `/bin/true` or any other binary resulting in immediate exit.)

```bash
docker run --rm -i -t \
    -e SAMBA_REALM="samba.dom" \
    -e SAMBA_PASSWORD="Password1!" \
    -e SAMBA_HOST_IP="192.168.1.10" \
    -e SAMBA_DNS_FORWARDER="192.168.1.1" \
    --volumes-from dc_data \
    pitkley/samba-ad-dc
```

## Environment variables

The following environment variables are all used as part of the DC setup process.
If the DC has been setup, none of these variables have any effect on the container!

- `SAMBA_REALM` (*required*) The realm (comparable to the FQDN) for the domain controller (e.q. `samba.dom`).
- `SAMBA_DOMAIN` (*optional*) The domain (comparable to the NetBios-name) for the domain controller (e.g. `samba`).
    If it is not supplied, the first part of the FQDN/`SAMBA_REALM` will be used.
- `SAMBA_PASSWORD` (*optional*) The password for the DC-Administrator.
    If not supplied, a random, 20 character long alphanumeric password will be generated and printed to stdout.
- `SAMBA_OPTIONS` (*optional*) Additional options for `samba-tool domain provision`.
- `SAMBA_HOST_IP` (*optional*) Set the IPv4 address during provisioning.
    (If you need to set a IPv6 address, supply `--host-ip6=IP6ADDRESS` through `SAMBA_OPTIONS`.)
- `SAMBA_DNS_FORWARDER` (*optional*) You can supply the dns-forwarder Samba will use to answer non-local DNS-requests clients submit.
- `SAMBA_SETUP_ONLY` (*optional*) If this variable is set to a arbitrary non-empty string, the container will stop (with a non-zero exit code!) after the setup has finished and does not launch samba/the domain controller.
    If the container is already setup, this variable has no effect.

