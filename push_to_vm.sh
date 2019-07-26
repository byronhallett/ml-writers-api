gcloud compute --project "cl-syd-ml-writers" scp \
  traefik.toml docker-compose.yml tmux.sh \
  bhallett@ml-api-vm-1:~ --zone "australia-southeast1-a"