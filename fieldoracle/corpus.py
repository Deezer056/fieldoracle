"""FieldOracle corpus — pests and diseases.

Fills the two biggest gaps in scripts/corpus.py, which covers varieties,
fertilizer, establishment, seasons and water but has nothing at all on pests
or diseases. Same shape as DOCS there: one retrievable idea per entry.

Every entry below was taken from a Sri Lanka Department of Agriculture page
(doa.gov.lk, Rice Research and Development Institute) and checked against it.
Where the DOA page does not state something — a scientific name, a threshold,
a spray rate — it is left out rather than filled in from elsewhere. An
invented agronomic figure is the exact failure this project exists to fix.

Batch 1 of 2. Still to come: weeds, water management through the growth
stages, 4-month and rainfed fertilizer schedules, harvesting.
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
]
