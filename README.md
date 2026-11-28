# outage-time-machine

A small networking lab that recreates the BGP route withdrawal behind a real CDN outage, allowing you to trigger the failure, observe the impact, and restore service yourself.

Independent educational project inspired by Cloudflare's February 2026 BYOIP outage post-mortem. Not affiliated with or endorsed by Cloudflare. All IP addresses and AS numbers used in this lab are reserved for documentation or private use.

## What happened

Cloudflare customers can bring their own IP address ranges (BYOIP) and have Cloudflare advertise those ranges to the Internet using BGP.

In February 2026, an automated cleanup task intended to remove customer prefixes marked for deletion encountered a bug. Instead of returning only prefixes pending deletion, the system returned all BYOIP prefixes. The task began withdrawing valid customer prefixes and removing associated configuration.

Approximately 1,100 prefixes were withdrawn, affecting around 25% of Cloudflare's BYOIP prefixes. Impacted services became unreachable, causing connection failures, timeouts, and website errors. Recovery involved restoring route advertisements and, in some cases, rebuilding missing service configuration.

## What this lab does

This lab recreates the control-plane failure pattern behind the outage using Containerlab, Docker, FRRouting (FRR), and a small Python automation script.

The topology consists of four containers:

client ── inet ── edge ── web

The edge router advertises a customer prefix over BGP, making the web server reachable through the simulated network. A Python cleanup task intentionally contains a logic bug that withdraws the customer prefix, reproducing the same class of routing failure described in the incident. The route can then be restored to simulate recovery.

## Network

client --- inet --- edge --- web

| Device | Address | ASN |
|----------|----------|----------|
| client | 203.0.113.10/24 | - |
| inet | 203.0.113.1/24, 192.0.2.2/30 | 64513 |
| edge | 192.0.2.1/30, 198.51.100.1/24 | 64512 |
| web | 198.51.100.10/24 | - |

# Deploy the lab
sudo containerlab deploy -t outage.clab.yml

# Verify connectivity
docker exec clab-outage-client ping -c 3 198.51.100.10

# Trigger the outage
python3 cleanup_task.py

# Restore the route
docker exec clab-outage-edge vtysh \
-c "configure terminal" \
-c "router bgp 64512" \
-c "address-family ipv4 unicast" \
-c "network 198.51.100.0/24"

# Destroy the lab
sudo containerlab destroy -t outage.clab.yml --cleanup