import gzip
import numpy as np
import pdb


test_set = ['amazon.com.ga.us', '4mazon.com', 'a.mazon.com', 'choppywingo.amazon.com.zip']
alexa_domains = ['amazon.com', 'boa.com', 'truist.com']


for test_val_full in test_set:
    # TODO: chop down test_val based on octets...like foo.bar.bp.com, bar.bp.com, bp.com
    domains_to_consider = []
    octets = test_val_full.split('.')
    octet_count = len(octets)
    for x in range(0, octet_count):
        if x < octet_count-1:
            domain_to_consider = ".".join(octets[x:octet_count])
            domains_to_consider.append(domain_to_consider)

    for test_val in domains_to_consider:
        gzip_one_len = len(gzip.compress(test_val.encode()))
        distance_from_test_val = []
        for training_val in alexa_domains:
            gzip_two_len = len(gzip.compress(training_val.encode()))
            catted_values = " ".join([test_val, training_val])
            catted_len = len(gzip.compress(catted_values.encode()))
            ncd = (catted_len - min(gzip_one_len, gzip_two_len)) / max(gzip_one_len, gzip_two_len)
            if ncd < .21:
                print(f'{test_val_full}->{test_val} resembles {training_val} Score: {ncd}')
            #else:
            #    print(f'no match for {test_val} compared to {training_val} Score: {ncd}')

        sorted_idx = np.argsort(np.array(distance_from_test_val))
        #top_k_class = alexa_domains[sorted_idx[:k], 1]
        #predict_class = max(set(top_k_class), key=top_k_class.count)

