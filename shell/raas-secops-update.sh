# script to update the secops packages for VMware Salt RAAS
# this script relies on the use of 1password to retrieve the Broadcom registry token required for software downloads
# run this script from the home directory - it should place downloads in the "Downloads" directory of the current user

rm -f ~/Downloads/locke_* ~/Downloads/vman_*
sudo rm -f /tmp/locke_* /tmp/vman_*

op run --env-file=<(echo "ACCESS_TOKEN=op://projects/broadcom/registry-token") -- \
podman run --rm -it \
  -v "${HOME}/Downloads:/downloads:z" \
  -w /downloads \
  -e ACCESS_TOKEN \
  releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:latest \
  sh -c "jf c add internal-server --url=https://packages.broadcom.com --access-token=\$ACCESS_TOKEN --interactive=false && \
         jf rt dl 'tis-saltcontent/secops/' --server-id=internal-server --sort-by=created  --sort-order=desc --limit=1 --flat"


op run --env-file=<(echo "ACCESS_TOKEN=op://projects/broadcom/registry-token") -- \
podman run --rm -it \
  -v "${HOME}/Downloads:/downloads:z" \
  -w /downloads \
  -e ACCESS_TOKEN \
  releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:latest \
  sh -c "jf c add internal-server --url=https://packages.broadcom.com --access-token=\$ACCESS_TOKEN --interactive=false && \
         jf rt dl 'tis-saltcontent/vman/' --server-id=internal-server --sort-by=created --sort-order=desc --limit=1 --flat"

sudo cp ./Downloads/locke_* /tmp
sudo cp ./Downloads/vman_* /tmp

sudo chown raas:raas /tmp/locke_* /tmp/vman_*

sudo -u raas /opt/saltstack/raas/bin/raas ingest /tmp/locke_*
sudo -u raas /opt/saltstack/raas/bin/raas vman_ingest /tmp/vman_*

