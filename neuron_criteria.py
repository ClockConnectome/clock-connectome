def getClock(l_lnv=False):
    """
    Manually generates table of the clock neurons with or without the l-lnvs
    """
    import pandas as pd

    clock_dictionary = {
       'bodyId': (2068801704, 1664980698, 2007068523, 1975347348, 5813056917, 5813021192, 5813069648, 511051477,
                  296544364, 448260940, 5813064789, 356818551, 480029788, 450034902, 546977514, 264083994, 5813022274,
                  5813010153, 324846570, 325529237, 387944118, 387166379, 386834269, 5813071319),
       'type': tuple(('s-LNv', 's-LNv', 's-LNv', 's-LNv', 'LNd', 'LNd', 'LNd', '5th s-LNv', 'LNd', 'LNd', 'LNd',
                'LPN', 'LPN', 'LPN', 'LPN', 'DN1a', 'DN1a', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pA', 'DN1pB', 'DN1pB')),
       'seqInstance': ['s-LNv_R_1', 's-LNv_R_2', 's-LNv_R_3', 's-LNv_R_4', 'LNd_R_4', 'LNd_R_5', 'LNd_R_6',
                    '5th s-LNv_R_1', 'LNd_R_1', 'LNd_R_2', 'LNd_R_3', 'LPN_R_1', 'LPN_R_2', 'LPN_R_3', 'LPN_R_4',
                    'DN1a_R_1', 'DN1a_R_2', 'DN1pA_R_1', 'DN1pA_R_2', 'DN1pA_R_3', 'DN1pA_R_4', 'DN1pA_R_5',
                    'DN1pB_R_1', 'DN1pB_R_2'],
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
           'phase': ['', '', '', ''],
           'phase_specific': ['', '', '', '']}
        
        l_lnv_df = pd.DataFrame.from_dict(l_lnv_dictionary)
        clock_df = clock_df.append(l_lnv_df, ignore_index=True)

    return clock_df

def bodyIds_by_type():
    ids_by_type = {'s-LNv':[1664980698, 1975347348, 2007068523, 2068801704],
    '5th s-LNv':511051477,
    'LNd':[296544364, 448260940, 5813021192, 5813056917, 5813064789, 5813069648],
    'LPN':[356818551, 450034902, 480029788, 546977514],
    'DN1a':[264083994, 5813022274],
    'DN1pA':[324846570, 325529237, 387166379, 387944118, 5813010153],
    'DN1pB':[386834269, 5813071319],
    'l-LNv': [1884625521,2065745704, 5813001741, 5813026773]}
    return ids_by_type

def define_neuron_criteria():
    # define the criteria for the 23 neurons in "The Big One"
    from neuprint import NeuronCriteria as NC

    sLNv_ID = [1664980698, 1975347348, 2007068523, 2068801704]
    sLNv_5_ID = [511051477]
    LNd_ID = [296544364, 448260940, 5813021192, 5813056917, 5813064789, 5813069648]
    LPN_ID = [356818551, 450034902, 480029788, 546977514]
    DN1a_ID = [264083994, 5813022274]
    DN1pA_ID = [324846570, 325529237, 387166379, 387944118, 5813010153]
    DN1pB_ID = [386834269, 5813071319]

    criteria = NC(bodyId=tuple(sLNv_5_ID + sLNv_ID + LNd_ID + LPN_ID + DN1a_ID + DN1pA_ID + DN1pB_ID))
    return criteria