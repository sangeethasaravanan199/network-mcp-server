import dns.resolver

def dns_lookup(domain, record_type="A"):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2      # each DNS query timeout
    resolver.lifetime = 4     # total time for the lookup

    try:
        answers = resolver.resolve(domain, record_type)
        return [str(r) for r in answers]
    except Exception as e:
        return [f"DNS lookup failed: {e}"]
