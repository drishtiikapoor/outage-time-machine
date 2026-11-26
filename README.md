# outage-time-machine

Customers can bring their own IP addresses (BYOIP) to Cloudflare. Cloudflare then advertises those range to the Internet, allowing traffic destined for those addresses to be routed through Cloudflare's network for protection and acceleration.

Removing a BYOIP prefix was historically a manual process. Cloudflare introduced an automated cleanup task that periodically searched for prefixes marked for deletion and removed them.

Due to a bug in the task's API request, the system returned all BYOIP prefixes instead of only those pending deletion. The cleanup task therefore treated every customer-owned prefix as eligible for removal and began deleting prefixes and their associated service bindings.

Approximately 1,100 prefixes, representing about 25% of Cloudflare's BYOIP prefixes, were withdrawn from the network. Services using those prefixes became unreachable, resulting in connection failures, timeouts, and 403 errors on the 1.1.1.1 website. The incident lasted over 6 hours.

Engineers identified and disabled the faulty task, preventing further withdrawals. Many affected customers restored service by re-advertising their prefixes through the Cloudflare dashboard. Remaining prefixes were restored by Cloudflare engineers, while prefixes that had lost their service bindings required a global configuration rollout across Cloudflare's edge network