# CSCI-Unsupervised-Project
Reconstructing RNA sequences using G and CU enzyme splits

Link to LIVE WEBSITE at pythonanywhere! : https://mnd1616.pythonanywhere.com/

When inputting RNA sequences for G-enzyme and CU-enzyme please be sure to enter everything in all caps seperated by comma and space after the comma. 
I.E.
G-Enzyme split : AUCG, AUG, G, CU, ACUAUACG             .... and the
CU-enzyme split : GGAC, U, AU, GAU, C, U, AC, GC, AU     ....

Returns will be : ['AUGAUCGGACUAUACGCU', 'AUCGAUGGACUAUACGCU', 'AUGGACUAUACGAUCGCU', 'AUCGGACUAUACGAUGCU']


Their is only one potential problem with the code. This has to do with two extra fragments in the singles extended bases when 
compared to the interiors extended bases. These two fragments are always the start and end. But disambiguating between 
the start and end is not clear. For this reason, for the above code to work, the following assumptions must be made.
Assumptions: 
1: The two extra fragments (in the singles versus the interior extended bases) have to be in the interior extended bases 
and have to be in the non single fragments. 2: The abnormal fragment from the g-enzyme has to carry in it either of the two extra 
fragments to be able to disambiguate between the start and end fragments. This disambiguation must make it clear as to which fragment
is the start and which is the end. If either of these assumptions fails then the code crumbles.

