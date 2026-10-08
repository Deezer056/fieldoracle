"""FieldOracle corpus — pests, diseases, fertilizer, weeds and water.

One retrievable idea per entry: a short self-contained passage, an id that is
stable so re-loading upserts rather than duplicates, a category for metadata
filtering, and the DOA page it came from.

Every entry below was taken from a Sri Lanka Department of Agriculture page
(doa.gov.lk, Rice Research and Development Institute) and checked against it.
Where the DOA page does not state something — a scientific name, a threshold,
a spray rate — it is left out rather than filled in from elsewhere. An
invented agronomic figure is the exact failure this project exists to fix.

Batch 1 covered pests and diseases. Batch 2 adds the four zone fertilizer
schedules, weeds, and water management.

Two notes on batch 2. First, the DOA fertilizer tables render with the Time
column merged, which shifts every basal row one cell left and makes the basal
TSP dose look like urea. The split quantities below were reassigned to the
column that makes all four of the page's own stated totals reconcile, and the
basal TSP figures were then confirmed independently against the RRDI
phosphorous fertilizer technology page. Second, a yield figure for Bg 750 that
appeared in the working notes could not be found on any DOA page on re-check,
so it was dropped and only the stated 75 day duration was kept.

Harvesting is still missing: RRDI has no harvesting page that states moisture
content or loss figures, and nothing was invented to fill the gap.
"""

DOCS = [
    # ---------------------------------------------------------------- pests
    {
        "id": "pest-bph-damage",
        "category": "pest",
        "source": "RRDI — Brown plant hopper, damage",
        "text": "Brown plant hopper (BPH) feeds on rice and heavy infestations produce "
                "hopper burn: leaves dry and turn brown after feeding, and patches of burned "
                "plants are often lodged. BPH also transmits grassy stunt virus and ragged "
                "stunt virus, so the insect causes damage both directly and as a disease vector.",
    },
    {
        "id": "pest-bph-threshold",
        "category": "pest",
        "source": "RRDI — Brown plant hopper, economic threshold",
        "text": "The economic threshold for brown plant hopper is 2 insects per hill at the "
                "booting stage and 5 per hill at the heading stage. These thresholds are adjusted "
                "upward where spider predator populations are high, because the spiders are "
                "already suppressing the hoppers. Below the threshold, spraying costs more than "
                "the damage it prevents.",
    },
    {
        "id": "pest-bph-control",
        "category": "pest",
        "source": "RRDI — Brown plant hopper, management",
        "text": "Brown plant hopper management: grow resistant varieties, drain the field to "
                "reduce moisture, avoid indiscriminate insecticide use during the vegetative "
                "stage because it kills the natural enemies that keep BPH down, monitor the crop "
                "regularly for early detection, and use effective insecticides only during an "
                "actual epidemic.",
    },
    {
        "id": "pest-bph-varieties",
        "category": "variety",
        "source": "RRDI — Brown plant hopper, resistant varieties",
        "text": "Rice varieties resistant to brown plant hopper include Bg 379-2, Bg 300, Bg 403, "
                "Bg 304, Bg 357, Bg 358 and Bg 360. Ptb 33 carries a high level of resistance and "
                "is used as the resistant check in screening.",
    },
    {
        "id": "pest-gallmidge-damage",
        "category": "pest",
        "source": "RRDI — Rice gall midge, damage",
        "text": "Rice gall midge larvae move down between the leaf sheaths until they reach the "
                "apical bud, lacerate the tissue and feed there until pupation. This forms a gall "
                "known as a silver shoot or onion shoot. A tiller that forms a gall stops "
                "developing and produces no panicle, so yield falls. Damage is high in wet, humid "
                "weather.",
    },
    {
        "id": "pest-gallmidge-control",
        "category": "pest",
        "source": "RRDI — Rice gall midge, management",
        "text": "In areas where rice gall midge is endemic, growing a resistant variety is the "
                "most economical control. Granular insecticides are recommended, but their value "
                "is limited in practice because farmers usually apply them only after the silver "
                "shoots are already visible, by which time the damage is done. Weed control is "
                "also effective, since weeds host the midge between crops.",
    },
    {
        "id": "pest-gallmidge-varieties",
        "category": "variety",
        "source": "RRDI — Rice gall midge, resistant varieties",
        "text": "Varieties resistant to rice gall midge biotype I include Bg 276-5, Bg 400-1, "
                "Bg 380, Bg 450 and Bg 300. Varieties resistant to both biotype I and biotype II "
                "include Bg 304, Bg 305, Bg 357, Bg 359 and Bg 360. Which biotype is present "
                "decides which list applies.",
    },

    # ------------------------------------------------------------- diseases
    {
        "id": "dis-blast-symptoms",
        "category": "disease",
        "source": "RRDI — Rice blast, symptoms",
        "text": "Rice blast is caused by the fungus Magnaporthe grisea (Pyricularia grisea). On "
                "leaves it makes spindle-shaped spots 1.0-1.5 cm long and 0.3-0.5 cm wide, with "
                "brown or reddish-brown margins, ashy grey centres and pointed ends. Infected nodes "
                "blacken and rot. Infection at the base of the panicle is called rotten neck or "
                "neck rot and produces whiteheads: the panicles go white and empty, standing pale "
                "above the green crop, and the grain in them is lost.",
    },
    {
        "id": "dis-blast-conditions",
        "category": "disease",
        "source": "RRDI — Rice blast, favourable conditions",
        "text": "Rice blast is favoured by low night temperatures of 17-20 degrees Celsius, high "
                "humidity, foggy and dark conditions, high plant density, and excessive nitrogen "
                "fertilizer. Over-applying urea is therefore a cause of blast, not a cure for it: "
                "the first management step during the season is to apply urea only at the "
                "recommended rate or according to the leaf colour chart.",
    },
    {
        "id": "dis-blast-fungicides",
        "category": "disease",
        "source": "RRDI — Rice blast, fungicide recommendations",
        "text": "If rice blast is spreading rapidly, the recommended fungicides and rates per 16 "
                "litres of water, applied at 8-10 tanks per acre, are: Tebuconazole 250 g/l EC at "
                "10 ml; Isoprothiolane 400 g/l EC at 20 ml; Carbendazim 50% WP or WG at 11 g; "
                "Tricyclazole 75% WP at 10 g. Fungicide is a response to active spread, not a "
                "routine application.",
    },
    {
        "id": "dis-blast-prevention",
        "category": "disease",
        "source": "RRDI — Rice blast, next season",
        "text": "To reduce rice blast in the following season: plant a resistant variety, use "
                "disease-free certified seed, incorporate 250 kg of burnt paddy husk per acre "
                "during land preparation, and do not plough in straw from a diseased crop.",
    },
    {
        "id": "dis-brownspot-symptoms",
        "category": "disease",
        "source": "RRDI — Brown spot, symptoms",
        "text": "Brown spot is caused by the fungus Cochliobolus miyabeanus (Bipolaris oryzae). "
                "It makes brown, circular to oval spots on the coleoptile that can cause seedling "
                "blight. On leaves the spots range from tiny dark marks to larger ovals with a "
                "dark brown margin and a light reddish-brown or grey centre. Infected glumes turn "
                "black, and affected florets give light or chalky kernels.",
    },
    {
        "id": "dis-brownspot-conditions",
        "category": "disease",
        "source": "RRDI — Brown spot, favourable conditions",
        "text": "Brown spot develops at temperatures of 16-36 degrees Celsius with humidity of "
                "86-100%. It is strongly associated with poor soil: low nutrient status, high "
                "salinity, iron toxicity, and drought stress. Brown spot is often a symptom of a "
                "soil problem rather than a disease to be sprayed away.",
    },
    {
        "id": "dis-brownspot-management",
        "category": "disease",
        "source": "RRDI — Brown spot, management",
        "text": "Brown spot management during the season is to apply urea at the recommended dose "
                "and control weeds. For the next season: apply organic fertilizer to improve soil "
                "condition, use disease-free certified seed, incorporate 250 kg of burnt paddy "
                "husk per acre at land preparation, treat seed by dipping in hot water at 53-54 "
                "degrees Celsius for 10-12 minutes or with a fungicide, rotate the crop, and level "
                "the land properly.",
    },
    {
        "id": "dis-narrowbrownspot",
        "category": "disease",
        "source": "RRDI — Narrow brown leaf spot",
        "text": "Narrow brown leaf spot is caused by the fungus Sphaerulina oryzina (Cercospora "
                "janseana). Lesions are light to dark brown, linear, run parallel to the leaf vein "
                "and measure about 2-10 mm long by 1-1.5 mm wide. On susceptible varieties they "
                "merge into larger dead areas, and a net blotch pattern of brown and yellowish "
                "areas appears on the leaf sheath. Brown lesions also form on glumes and pedicels. "
                "Severity increases as the crop approaches maturity.",
    },
    {
        "id": "dis-narrowbrownspot-management",
        "category": "disease",
        "source": "RRDI — Narrow brown leaf spot, management",
        "text": "Narrow brown leaf spot management during the season is to apply urea at the "
                "recommended rate or by leaf colour chart. For the next season: apply organic "
                "fertilizer to improve soil condition, plant certified disease-free seed, manage "
                "weeds properly, incorporate 250 kg of burnt paddy husk per acre at land "
                "preparation, and do not plough in diseased straw.",
    },
    {
        "id": "dis-common-practice",
        "category": "disease",
        "source": "RRDI — Practices common to rice fungal diseases",
        "text": "Four practices appear in the recommendations for rice blast, brown spot and "
                "narrow brown leaf spot alike: apply urea only at the recommended rate or by leaf "
                "colour chart rather than over-fertilising, use certified disease-free seed, "
                "incorporate 250 kg of burnt paddy husk per acre during land preparation, and do "
                "not incorporate straw from a diseased crop. Doing these four removes most "
                "routine fungal pressure before any spraying is considered.",
    },
    {
        "id": "dis-differential-whiteheads",
        "category": "disease",
        "source": "RRDI — composed from the rice blast and brown spot pages",
        "text": "If the panicles go white and empty while the rest of the plant is still "
                "green, that points to rice blast infecting the base of the panicle — neck rot, "
                "which produces whiteheads. Brown spot does not kill panicles this way: it "
                "blackens the glumes and gives light or chalky kernels, but the panicle still "
                "fills. White empty panicles standing above a green crop are the symptom that "
                "separates blast from brown spot.",
    },
    {
        "id": "dis-differential-leafspots",
        "category": "disease",
        "source": "RRDI — composed from the blast, brown spot and narrow brown leaf spot pages",
        "text": "Three rice leaf spots are told apart by the shape of the lesion. Rice blast makes "
                "spindle-shaped spots with pointed ends, 1.0-1.5 cm long and 0.3-0.5 cm wide, with "
                "ashy grey centres and brown or reddish-brown margins. Brown spot makes circular to "
                "oval spots with a dark brown margin and a light reddish-brown or grey centre. "
                "Narrow brown leaf spot makes thin linear lesions that run parallel to the vein, "
                "about 2-10 mm long and only 1-1.5 mm wide. Pointed and spindle means blast; round "
                "or oval means brown spot; thin and linear means narrow brown leaf spot.",
    },
    # ------------------------------------------------------------ fertilizer
    {
        "id": "fert-irrigated-izdz",
        "category": "fertilizer",
        "source": "DOA - Fertilizer recommendation, irrigated, intermediate and dry zone",
        "text": "For irrigated paddy in the intermediate and dry zones the recommendation per "
                "hectare is 225 kg urea, 55 kg TSP, 60 kg MOP and 5 kg zinc sulphate. The whole "
                "TSP dose and the whole zinc sulphate dose go on as basal at establishment. Urea "
                "is then split four ways: 50 kg at 2 weeks, 75 kg at 4 weeks, 65 kg at 6 weeks "
                "and 35 kg at 7 weeks. MOP is split twice: 25 kg at 4 weeks and 35 kg at 6 weeks. "
                "All weeks are counted from the date of establishment. These timings are for a "
                "3 month variety.",
    },
    {
        "id": "fert-irrigated-izdz-longer",
        "category": "fertilizer",
        "source": "DOA - Fertilizer recommendation, irrigated, intermediate and dry zone",
        "text": "A longer variety changes the dates of the irrigated intermediate and dry zone "
                "schedule but not the quantities. The final 35 kg of urea goes on at 7 weeks for a "
                "3 month crop, 8 weeks for a 3.5 month crop and 9 weeks for a 4 month crop. For "
                "the 4 month crop the third urea split and the second MOP split also move out from "
                "6 weeks to 7 weeks. The totals stay 225 kg urea, 55 kg TSP, 60 kg MOP and 5 kg "
                "zinc sulphate per hectare for all three crop ages.",
    },
    {
        "id": "fert-rainfed-izdz",
        "category": "fertilizer",
        "source": "DOA - Fertilizer recommendation, rainfed, intermediate and dry zone",
        "text": "For rainfed paddy in the intermediate and dry zones the recommendation per "
                "hectare is 175 kg urea, 35 kg TSP, 50 kg MOP and 5 kg zinc sulphate, which is "
                "less of every nutrient than the irrigated schedule for the same zones. TSP and "
                "zinc sulphate go on basal. Urea is split 30 kg at 2 weeks, 65 kg at 4 weeks, "
                "50 kg at 6 weeks, and 30 kg at 7 weeks for a 3 month crop or 8 weeks for a "
                "3.5 month crop. MOP is split 25 kg at 4 weeks and 25 kg at 6 weeks. The DOA page "
                "gives this schedule for 3 month and 3.5 month crops only - there is no 4 month "
                "rainfed table for these zones.",
    },
    {
        "id": "fert-irrigated-wz",
        "category": "fertilizer",
        "source": "DOA - Fertilizer recommendation, irrigated, wet zone",
        "text": "For irrigated paddy in the wet zone the recommendation per hectare is 140 kg "
                "urea, 35 kg TSP, 50 kg MOP and 5 kg zinc sulphate. TSP and zinc sulphate go on "
                "basal. Urea is split 20 kg at 2 weeks, 55 kg at 4 weeks, 45 kg at 6 weeks and "
                "20 kg at 7 weeks, with the last two splits moving to 7 and 9 weeks for a 4 month "
                "crop. MOP is split 25 kg at 4 weeks and 25 kg at 6 weeks. The wet zone irrigated "
                "nitrogen rate is well below the intermediate and dry zone irrigated rate of "
                "225 kg urea.",
    },
    {
        "id": "fert-rainfed-wz",
        "category": "fertilizer",
        "source": "DOA - Fertilizer recommendation, rainfed, wet zone",
        "text": "For rainfed paddy in the wet zone the recommendation per hectare is 100 kg urea, "
                "55 kg TSP, 110 kg MOP and 5 kg zinc sulphate. This is the only one of the four "
                "DOA zone schedules in which potassium exceeds nitrogen. TSP and zinc sulphate go "
                "on basal. Urea is split 25 kg at 2 weeks, 30 kg at 4 weeks, 25 kg at 6 weeks and "
                "20 kg at 7 weeks. MOP is split three ways rather than two: 35 kg at 2 weeks, "
                "45 kg at 4 weeks and 30 kg at 6 weeks.",
    },
    {
        "id": "fert-zone-comparison",
        "category": "fertilizer",
        "source": "DOA - composed from the four zone fertilizer recommendation tables",
        "text": "Urea rates differ more than twofold across the four DOA paddy schedules: 225 kg "
                "per hectare for intermediate and dry zone irrigated, 175 kg for intermediate and "
                "dry zone rainfed, 140 kg for wet zone irrigated and 100 kg for wet zone rainfed. "
                "So the zone and the water regime must both be established before any fertilizer "
                "rate is quoted. Giving the 225 kg figure to a rainfed wet zone farmer would "
                "overstate nitrogen by more than double.",
    },
    {
        "id": "fert-tsp-conflict",
        "category": "fertilizer",
        "source": "DOA - RRDI soil science technology page vs the zone recommendation tables",
        "text": "Two DOA sources conflict on the TSP rate. The RRDI soil science technology page "
                "states 55 kg per hectare for irrigated paddy and 35 kg per hectare for rainfed "
                "paddy. The zone tables agree with that for the intermediate and dry zones, but "
                "reverse it for the wet zone, where the irrigated table gives 35 kg and the "
                "rainfed table gives 55 kg. The conflict cannot be resolved from the published "
                "pages, so a wet zone TSP rate should be confirmed with the local Agrarian "
                "Services Centre rather than quoted from a single page.",
    },
    {
        "id": "fert-tsp-soil-test",
        "category": "fertilizer",
        "source": "RRDI - Phosphorous fertilizer technology",
        "text": "TSP use can sometimes be halved. RRDI reports saving 50 percent of the TSP "
                "applied to paddy by applying phosphorus at the recommended rate only in the Yala "
                "season, and states this can be practised when the soil phosphorus level is above "
                "5 mg/kg. It is conditional on a soil test: without a measured soil phosphorus "
                "figure, the full rate for every season stands.",
    },
    # ----------------------------------------------------------------- weeds
    {
        "id": "weed-critical-period",
        "category": "weed",
        "source": "RRDI - Integrated weed management in paddy",
        "text": "The critical period of weed competition in rice begins 2 weeks after sowing and "
                "persists up to 5 to 8 weeks. Weeding inside that window protects yield; the same "
                "work done afterwards largely does not, because the crop has already lost the "
                "growth it was going to lose. This is why the recommended herbicide timings all "
                "fall between 0 and 28 days after sowing.",
    },
    {
        "id": "weed-damage",
        "category": "weed",
        "source": "RRDI - Damages caused by weeds",
        "text": "Weeds harm rice in three ways. Below ground they compete for water and nutrients, "
                "helped by runners and prostrate growth patterns that spread them through the "
                "field. Above ground they develop rapidly, shade the rice plants and hinder light "
                "acquisition. And the extra growth develops microenvironments that facilitate pest "
                "lifecycles, so a weedy field tends to become a pest-prone field as well.",
    },
    {
        "id": "weed-major-grasses",
        "category": "weed",
        "source": "RRDI - Major weeds in rice fields",
        "text": "RRDI lists these as major grass weeds of Sri Lankan rice fields: Echinochloa "
                "colona, Echinochloa crus-galli, Panicum repens, Ischaemum rugosum, Isachne "
                "globosa, Fimbristylis dichotoma, Paspalum distichum and Haeranthus africanus.",
    },
    {
        "id": "weed-major-sedges",
        "category": "weed",
        "source": "RRDI - Major weeds in rice fields",
        "text": "RRDI lists these as major sedge weeds of Sri Lankan rice fields: Cyperus iria, "
                "Cyperus difformis, Cyperus rotundus, Fimbristylis miliacea, Linderina spp. and "
                "Schoenoplectus supinus.",
    },
    {
        "id": "weed-major-broadleaf",
        "category": "weed",
        "source": "RRDI - Major weeds in rice fields",
        "text": "RRDI lists these as major broadleaved weeds of Sri Lankan rice fields: Commelina "
                "diffusa, Eclipta alba, Eichhornia crassipes, Monochoria vaginalis, Murdannia "
                "nudiflora, Sphenoclea zeylanica and Ludwigia perennis.",
    },
    {
        "id": "weed-list-caveat",
        "category": "weed",
        "source": "RRDI - Major weeds in rice fields, with a note on two entries",
        "text": "Two entries on the RRDI major weeds list sit in the wrong group. Fimbristylis "
                "dichotoma is listed under grasses, although Fimbristylis is a sedge genus and "
                "Fimbristylis miliacea is listed under sedges on the same page. Linderina spp. is "
                "listed under sedges and is most likely Lindernia, a broadleaved genus. Which "
                "group a weed belongs to - grass, sedge or broadleaf - decides which herbicide "
                "will work on it, so these two names should be checked against an actual specimen "
                "before a herbicide is chosen on the strength of the list alone.",
    },
    {
        "id": "weed-echinochloa-crusgalli",
        "category": "weed",
        "source": "RRDI - Echinochloa crus-galli",
        "text": "Echinochloa crus-galli (L.) P. Beauv, family Poaceae, is known in Sinhala as "
                "S-bajiri, maratu and wel-marakku, in Tamil as kutirai and val-pul, and in English "
                "as common barnyardgrass. It is erect and tufted, reclining at the base, and "
                "reaches up to 200 cm. The stems are cylindrical with a white spongy pith, the "
                "leaves are linear and 10 to 40 cm long, and the inflorescence is a compound "
                "raceme 10 to 25 cm long, green to purplish, with elliptical pointed slightly "
                "hairy spikelets. It flowers throughout the year, produces seed within 60 days, "
                "and prefers moist to wet conditions. RRDI calls it a serious weed of lowland rice.",
    },
    {
        "id": "weed-echinochloa-control",
        "category": "weed",
        "source": "RRDI - Echinochloa crus-galli, control",
        "text": "Hand weeding works poorly against Echinochloa crus-galli because at early growth "
                "stages it closely resembles the rice plant, so it is either missed or the rice is "
                "pulled with it. RRDI recommends proper land preparation, under wet or dry "
                "conditions, together with recommended herbicides instead. Its rapid growth, "
                "competitive ability and rapid multiplication are what make it a serious weed.",
    },
    {
        "id": "weed-iwm-methods",
        "category": "weed",
        "source": "RRDI - Integrated weed management practices",
        "text": "RRDI sets out integrated weed management in five groups. Preventive: use clean "
                "seed, keep the seed bed weed free, and maintain irrigation infrastructure and "
                "equipment cleanliness. Mechanical: rotary and other mechanical weeders, hand "
                "weeding, hoeing, tillage, harrowing and mowing. Cultural: proper land "
                "preparation, water management, fertilizer application in the recommended dose, "
                "suitable variety selection, timely sowing and plant density management. "
                "Biological: mulching, and breeding for competitiveness. Chemical: recommended "
                "herbicides.",
    },
    {
        "id": "weed-herbicide-oneshot",
        "category": "weed",
        "source": "DOA - Recommended herbicides for paddy, one-shot group",
        "text": "DOA one-shot herbicides for paddy, with rates per 16 litre tank and timing in days "
                "after sowing: pretilachlor 300 g/l EC, sold as Sofit 30EC, 64 to 80 ml at 0 to 3 "
                "days; oxyfluorfen 240 g/l EC, sold as Goal 2XL or Galigan, 4 ml at 2 to 3 days; "
                "pyrazosulfuron-ethyl 10 percent WP, sold as Sirius, 8.96 to 11.2 g at 7 to 14 "
                "days. All three are broad spectrum.",
    },
    {
        "id": "weed-herbicide-grass",
        "category": "weed",
        "source": "DOA - Recommended herbicides for paddy, grass killers",
        "text": "DOA grass herbicides for paddy, with rates per 16 litre tank and timing in days "
                "after sowing: cyhalofop-butyl 100 g/l EC, sold as Clincher 10EC, 80 to 102.4 ml "
                "at 15 to 21 days; metamifop 10 percent EC, sold as Matari, 52.8 ml at 21 days; "
                "fenoxaprop-p-ethyl 75 g/l EW, sold as Whip Super 7.5EW, 14.4 to 17.6 ml at 16 to "
                "25 days. These control grasses only - they will not deal with sedges or "
                "broadleaved weeds.",
    },
    {
        "id": "weed-herbicide-sedge-broadleaf",
        "category": "weed",
        "source": "DOA - Recommended herbicides for paddy, sedge and broadleaf killers",
        "text": "DOA herbicides for sedges and broadleaved weeds in paddy, with rates per 16 litre "
                "tank and timing in days after sowing: MCPA 400 g/l SL, sold as M40, 112 to "
                "140.08 ml at 21 to 28 days; MCPA 600 g/l SL, sold as M60, 72 to 89.6 ml at 21 to "
                "28 days. The two products are the same active ingredient at different strengths, "
                "so the rate has to be matched to the formulation written on the label.",
    },
    {
        "id": "weed-herbicide-rotation",
        "category": "weed",
        "source": "DOA - Recommended herbicides for paddy",
        "text": "The DOA herbicide recommendation stresses rotating herbicides with different modes "
                "of action to prevent weed resistance. Using the same product season after season "
                "selects for the weeds that survive it. Because the recommended list separates "
                "one-shot, grass-only and sedge-and-broadleaf products with different application "
                "windows, a rotation can be built from within the recommendation itself.",
    },
    # ----------------------------------------------------------------- water
    {
        "id": "water-requirement-formula",
        "category": "water",
        "source": "RRDI - Water management in lowland rice",
        "text": "The seasonal water requirement of a paddy field is the sum of daily "
                "evapotranspiration plus the sum of daily seepage and percolation. Both terms are "
                "field specific: evapotranspiration follows the weather and the growth stage, "
                "while seepage and percolation follow the soil. This is why two fields in the same "
                "irrigation scheme growing the same variety can need different amounts of water.",
    },
    {
        "id": "water-maha-requirement",
        "category": "water",
        "source": "RRDI - Water management in lowland rice, Maha figures from ARS Mahailluppallama",
        "text": "Measured Maha season water requirements at Agriculture Research Station "
                "Mahailluppallama differ by soil and crop age. On moderately drained Reddish Brown "
                "Earth a 3 month crop needed 1057 mm and a 4 month crop 1232 mm. On Low Humic Gley "
                "soils the figures were 948 mm for a 3 month crop and 1128 mm for a 4 month crop. "
                "The longer crop needs roughly 175 to 180 mm more water in either soil, and the "
                "Low Humic Gley soils need about 100 mm less than the Reddish Brown Earth.",
    },
    {
        "id": "water-saturated-saving",
        "category": "water",
        "source": "RRDI - Water management, mitigation options",
        "text": "Maintaining a saturated condition instead of standing water could save up to 40 "
                "percent of water in clay loam soils without reducing yield, according to RRDI. "
                "The saving comes from cutting percolation and seepage losses rather than from "
                "reducing what the crop transpires, which is why the figure is tied to a soil "
                "type and should not be assumed for sandy or well drained fields.",
    },
    {
        "id": "water-mitigation-options",
        "category": "water",
        "source": "RRDI - Water management, mitigation options",
        "text": "RRDI mitigation options for water short conditions in paddy include: shortening "
                "land preparation time using total killing herbicides such as paraquat; dry sowing "
                "in well drained or sandy soils where water use is very high; mulching straw after "
                "seeding to conserve moisture, which also gives earlier and more uniform "
                "germination and suppresses weeds; careful plastering of the bunds and thorough "
                "puddling of the field to avoid rapid percolation and lateral seepage; and timely "
                "cultivation that starts land preparation with the onset of the rains so that "
                "rainfall is used instead of irrigation water.",
    },
    {
        "id": "water-short-age-varieties",
        "category": "water",
        "source": "RRDI - Water management, mitigation options",
        "text": "Variety choice is one of the RRDI responses to a short or unreliable water supply. "
                "Bg 750, a 75 day variety, is named for drought prone areas, and the Kakulan type "
                "62-355, which has weed competitive ability, is named for short growing seasons. "
                "A shorter crop finishes before the water runs out; the DOA zone fertilizer tables "
                "also show a 3 month crop takes its last top dressing at 7 weeks rather than 9.",
    },
]
