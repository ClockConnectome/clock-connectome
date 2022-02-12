def getClock(l_lnv=False):
    """
    Manually generates table of the clock neurons with or without the l-lnvs

    :param l_lnv: default false. If set to True, includes information about l-lnv neurons.
    :return: (Dataframe) of clock neuron information
    """
    import pandas as pd

    clock_dictionary = {
       'bodyId': [2068801704, 1664980698, 2007068523, 1975347348, 5813056917, 5813021192, 5813069648, 511051477,
                  296544364, 448260940, 5813064789, 356818551, 480029788, 450034902, 546977514, 264083994, 5813022274,
                  5813010153, 324846570, 325529237, 387944118, 387166379, 386834269, 5813071319],
       'type': ['s-LNv', 's-LNv', 's-LNv', 's-LNv', 'LNd', 'LNd', 'LNd', '5th s-LNv', 'LNd', 'LNd', 'LNd',
                'LPN', 'LPN', 'LPN', 'LPN', 'DN1a', 'DN1a', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pB', 'DN1pB'],
       'seqInstance': ['s-LNv_R_1', 's-LNv_R_2', 's-LNv_R_3', 's-LNv_R_4', 'LNd_R_4', 'LNd_R_5', 'LNd_R_6',
                    '5th s-LNv_R_1', 'LNd_R_1', 'LNd_R_2', 'LNd_R_3', 'LPN_R_1', 'LPN_R_2', 'LPN_R_3', 'LPN_R_4',
                    'DN1a_R_1', 'DN1a_R_2', 'DN1pA_R_1', 'DN1pA_R_2', 'DN1pA_R_3', 'DN1pA_R_4', 'DN1pA_R_5',
                    'DN1pB_R_1', 'DN1pB_R_2'],
       'labels': ['sLNv1', 'sLNv2', 'sLNv3', 'sLNv4', 'LNd4', 'LNd5', 'LNd6',
                    '5th sLNv', 'LNd1', 'LNd2', 'LNd3', 'LPN1', 'LPN2', 'LPN3', 'LPN4',
                    'DN1a1', 'DN1a2', 'DN1pA1', 'DN1pA2', 'DN1pA3', 'DN1pA4', 'DN1pA5',
                    'DN1pB1', 'DN1pB2'],
       'phase': ['morning', 'morning', 'morning', 'morning', 'evening', 'evening', 'evening', 'evening', 'evening', 
                 'evening', 'evening', '', '', '', '', '', '', '', '', '', '', '', '', ''],
       'subphase': ['M', 'M', 'M', 'M', 'E1', 'E1', 'E2', 'E2', 'E3', 
                 'E3', 'E3', '', '', '', '', '', '', '', '', '', '', '', '', '']}
    #additional field w clock labels stylized w/o R or without underscore
    clock_df = pd.DataFrame.from_dict(clock_dictionary)

    if l_lnv:
        l_lnv_dictionary = {
           'bodyId': (1884625521,2065745704, 5813001741, 5813026773),
           'type': tuple(('l-LNv', 'l-LNv', 'l-LNv', 'l-LNv')),
           'seqInstance': ['l-LNv_R_1', 'l-LNv_R_2', 'l-LNv_R_3', 'l-LNv_R_4'],
           'labels': ['lLNv1', 'lLNv2', 'lLNv3', 'lLNv4'],
           'phase': ['', '', '', ''],
           'subphase': ['', '', '', '']}
        
        l_lnv_df = pd.DataFrame.from_dict(l_lnv_dictionary)
        clock_df = clock_df.append(l_lnv_df, ignore_index=True)

    return clock_df

def bodyIds_by_type(clock_df):
    """
    Uses data from clock_df to return a dictionary mapping neurons to lists of bodyIds.
    :param clock_df: clock information dataframe
    :return: (Dictionary) of body ids by clock type
    """
    from collections import defaultdict

    ids_by_type = defaultdict()
    for t in clock_df.type.unique():
        one_type = clock_df[clock_df['type']==t]
        body_ids = one_type['bodyId']
        body_ids = body_ids.values.tolist()
        ids_by_type[t] = body_ids
    return ids_by_type