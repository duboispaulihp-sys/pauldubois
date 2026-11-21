VHC CALIBRATION OF THE LEDGER MODEL (h(A)^boxtimes n)
live = ledger + sum_{sigma_1>=5} b_sigma^2 ; exact integers
============================================================================

-- 1. The zero window: P_k(n) for k = 1..4 --
   P_k(n) = 0 for all n = 2..16, k = 1..4: True  (binomial phase; the caps bind only from k = 5)
   -> the model's variational content starts at degree k = 5 in every
      column: the birth of the first syzygy square b_(5)(n)^2.

-- 2. Syzygy census P_k(n), n = 2..16, k = 1..9 --
     n: k=1  k=2  k=3  k=4  k=5  k=6  k=7  k=8  k=9
    2: 0  0  0  0  16  18  12  4  0   (0.0s)
    3: 0  0  0  0  324  1202  2457  3411  3175   (0.0s)
    4: 0  0  0  0  2704  21008  86288  243564  513344   (0.0s)
    5: 0  0  0  0  14641  194225  1333625  6256175  22267950   (0.1s)
    6: 0  0  0  0  60516  1221876  12616056  88436376  471070016   (0.1s)
    7: 0  0  0  0  207025  5909449  85613230  837883536  6221124525   (0.1s)
    8: 0  0  0  0  614656  23559200  456032384  5940866676  58587881600   (0.1s)
    9: 0  0  0  0  1633284  80924148  2017920276  33769354572  426937538372   (0.1s)
   10: 0  0  0  0  3968064  246814650  7707242700  161171679600  2541822351200   (0.1s)
   11: 0  0  0  0  8952064  682961994  26110424109  667384845919  12846247154939   (0.1s)
   12: 0  0  0  0  18974736  1742270288  80057442960  2456258997456  56684654949120   (0.1s)
   13: 0  0  0  0  38130625  4148228201  225599350769  8183856269901  223084825369120   (0.1s)
   14: 0  0  0  0  73170916  9307347140  591343775048  25040694499184  796144533102464   (0.1s)
   15: 0  0  0  0  134861769  19831648725  1455693686550  71168597759250  2610677893581875   (0.1s)
   16: 0  0  0  0  239878144  40382337664  3391595943424  189623183728464  7950251130118144   (0.1s)

-- 3. Syzygy square counts p(k) - p_4(k): independent Weil-type slots --
     k:      5      6      7      8      9
            1      2      4      7     12

-- 4. Ledger share ledger(k,n)/live(k,n) at the frontier columns --
   n = 8:
     k = 5: 1 - ledger/live = 49/830
     k = 6: 1 - ledger/live = 15025/75987
     k = 7: 1 - ledger/live = 3562753/9197811
     k = 8: 1 - ledger/live = 1485216669/2553114214
     k = 9: 1 - ledger/live = 91543565/122908184

   n = 12:
     k = 5: 1 - ledger/live = 1089/31714
     k = 6: 1 - ledger/live = 1799866/14164281
     k = 7: 1 - ledger/live = 4594665/16824724
     k = 8: 1 - ledger/live = 1127758952/2528847565
     k = 9: 1 - ledger/live = 5855852784/9531165755

   n = 16:
     k = 5: 1 - ledger/live = 234256/9301695
     k = 6: 1 - ledger/live = 315487013/3236215535
     k = 7: 1 - ledger/live = 6624210827/30261756065
     k = 8: 1 - ledger/live = 3950482994343/10596771642410
     k = 9: 1 - ledger/live = 970489639907/1816578265040

-- 5. Read --
   The zero window k<=4 = the model's proven 'divisor VHC'; every
   nonvanishing P_k(n) entry is one Weil-type slot per shape sigma_1>=5,
   and the certificates of the uploaded document (birth law, square
   decomposition, mirror law, Newton forms -- all audited digit-exactly
   in notes/03) are exactly the model's inductive VHC-proof pattern:
   propagate algebraicity column by column by closed laws.
