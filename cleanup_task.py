import subprocess
 
EDGE = "clab-outage-edge"
CUSTOMER_PREFIXES = ["198.51.100.0/24"]
PENDING_DELETE = []   # blocks customers actually asked to remove: none
 
def prefixes_to_delete(pending):
    # BUG: an empty list counts as "no filter", so everything matches
    if not pending:
        return CUSTOMER_PREFIXES
    return [p for p in CUSTOMER_PREFIXES if p in pending]
 
def withdraw(prefix):
    cmds = ["configure terminal", "router bgp 64512",
            "address-family ipv4 unicast", f"no network {prefix}"]
    args = ["docker", "exec", EDGE, "vtysh"]
    for c in cmds:
        args += ["-c", c]
    subprocess.run(args, capture_output=True, text=True)
    print(f"withdrew {prefix}")
 
print("cleanup task started")
for prefix in prefixes_to_delete(PENDING_DELETE):
    withdraw(prefix)
print("cleanup task finished")
