#!/usr/bin/env python
#################################################################
# DNS Digger
# Python Implemetation for DIG
# By: Yahia Kandil<yahia.kandil@gmail.com>
#################################################################
# DNS Types:
# qTypes = { 1:'A', 2:'NS', 5:'CNAME', 6:'SOA',
#           12:'PTR', 15:'MX', 16:'TXT', 28:'AAAA'}

# DNS Flags
# AA    Authoritative Answer    dns.flags.AA
# TC    Truncated response      dns.flags.TC
# RD    Recursion Desired       dns.flags.RD
# RA    Recursion Available     dns.flags.RA
# AD    Authentic Data          dns.flags.AD
# CD    Checking  DNSSEC        dns.flags.CD

# DNS rcode
# 0     NoError     No Error
# 1     FormErr     Format Error
# 2     ServFail    Server Failure
# 3     NXDomain    Non-Existent Domain
# 4     NotImp      Not Implemented
# 5     Refused     Query Refused

import dns.query
import dns.resolver
import dns.reversename
import collections
import tldextract


# Defaults
ns = '8.8.8.8'
timeout = 5


def __rrset_decoder(rrset):
    '''RRSet Decoder'''

    result = {
        'type': rrset.rdtype,
        'ttl': rrset.ttl,
        'name': str(rrset.name),
        'items': [str(rr) for rr in rrset.items]
    }

    return result


def dig(query, query_type=1, ns=ns, flags=0):
    '''Python Dig'''

    # Response Sections & Results
    sections = collections.defaultdict(list)
    result = collections.defaultdict(dict)

    # Domain Lower:
    query = query.lower()

    # Which NS is Queries
    result['ns'] = ns

    # Question
    result['q'] = {'query': query, 'query_type': query_type}

    # Construct Request
    try:
        request = dns.message.make_query(query, query_type)
        request.flags |= flags

    except Exception, e:
        result['error'] = str(e)
        return result

    # Get Response
    try:
        response = dns.query.udp(request, ns, timeout=timeout)

    except dns.exception.Timeout:
        result['error'] = 'TIMEOUT'
        return result

    # Getting Query Status
    rcode = response.rcode()
    result['rcode'] = rcode

    # If No Errors, get all rrsets
    if rcode == dns.rcode.NOERROR:
        sections['au'] = response.authority
        sections['ad'] = response.additional
        sections['an'] = response.answer

        # Process each rrset
        for section, rrsets in sections.iteritems():

            for rrset in rrsets:
                # Decode RRSet
                drrset = __rrset_decoder(rrset)
                name = drrset['name']
                result[section][name] = result[
                    section].get(name, []) + [drrset]

    return dict(result)


def get_ns(fqdn):
    '''Get Name Servers for Given fqdn'''
    nameservers = collections.defaultdict(list)

    # fqdn Fix:
    fqdn = fqdn.lower()

    # Get domain
    domain = tldextract.extract(fqdn).registered_domain + '.'

    # Get answers
    result = dig(domain, query_type=2, ns=ns)

    # Decode result
    answers = result.get('an', [])
    rcode = result.get('rcode', -1)
    additional = result.get('ad', [])

    # Get IP addresses for each nameserver
    if answers and rcode == dns.rcode.NOERROR:

        for rrset in answers[domain]:

            for nameserver in rrset['items']:

                # If the nameserver IP in additional, then get it
                if nameserver in additional:
                    items = []

                    for x in additional[nameserver]:
                        items += x['items']

                    # = nameservers.get(nameserver, []) + items
                    nameservers[nameserver].extend(items)

                # else dig the ns for the IP
                else:

                    try:
                        nameservers[nameserver] = dig(nameserver, ns=ns)['an'][
                            nameserver][0]['items']

                    except Exception, e:
                        print "Can't resolev", nameserver
                        print e

    # Return rcode & NameServers
    return rcode, dict(nameservers)


def dig_ns(domain):
    '''Dig Authoritative NameServer'''

    # Get NameServers
    rcode, nameservers = get_ns(domain)

    # Result
    result = {
        'nameservers': nameservers,
        'rcode': rcode
    }

    # Choose one from the NS Servers, and dig it for answer
    if rcode == dns.rcode.NOERROR:

        for nameserver, ip_addresses in nameservers.iteritems():

            # Query the nameserver
            result = dig(domain, ns=ip_addresses[0],
                         query_type=1, flags=dns.flags.AD)

            # If Found Return The Result
            return result

    else:
        print 'No NameServers: ' + domain

    return dict(result)
