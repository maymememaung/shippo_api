import shippo

shippo.config.api_key = "shippo_test_4be2330f4cc15d6d278b60de93c2adbc7ded0d1d"

address1 = shippo.Address.create(
    name='John Smith',
    street1='6512 Greene Rd.',
    street2='',
    company='Initech',
    phone='+1 234 346 7333',
    city='Woodridge',
    state='IL',
    zip='60517',
    country='US',
    metadata='Customer ID 123456'
)

print ('Success with Address 1 : %r' % (address1, ))