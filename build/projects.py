"""Project write-ups for the portfolio pages, taken from each maker's build book.

Each project: slug, title, subtitle (character · source), event, cover image,
facts (label, value), intro paragraphs, optional quote, and sections. A section
holds paragraphs, optional tables/lists, and gallery images (file stem, caption).
Images live in <person>/<slug>/img/<stem>.jpg (large) and <stem>-sm.jpg (thumbnail).
"""

CARRIE = [
  dict(
    slug='spin-the-dawn', year='2026', title='Spin the Dawn', card='The Blood of the Stars wedding dress',
    subtitle='Maia Tamarin · Spin the Dawn by Elizabeth Lim', event='Dragon Con Page to Stage · Journeyman', cover='i-000',
    facts=[('Character', 'Maia Tamarin'), ('Source', 'Spin the Dawn, Elizabeth Lim (2019)'), ('Contest', 'Dragon Con Page to Stage'), ('Skill tier', 'Journeyman'), ('Cost', 'About $200'), ('Pattern', 'Self-designed')],
    intro=[
      "In Elizabeth Lim’s Spin the Dawn, Maia Tamarin competes to become the imperial tailor and is given an impossible task: sew three magical gowns embodying the three children of the mother goddess Amana, the Sun, the Moon and the Stars, woven from the laughter of the Sun, the tears of the Moon and the blood of the Stars.",
      "This build interprets the bridal dress of the Stars: an iridescent color-shift gown of deep night, worn under a black glittering veil and a black-as-night robe whose interior carries an appliqué scene of Amana’s children, as told in the old monk’s legend. Closed, the robe reads as night sky. Opened, it reveals the whole mythology.",
    ],
    quote='As the Moon cries, the Sun laughs, and the Stars bleed; it painted such a beautiful picture in my mind. This was my inspiration in the making.',
    sections=[
      dict(title='Design and pattern drafting', paras=[
        "It began with a single concept sketch of the whole bridal gown: veil, robe, and the blood of the Stars raining down the skirt. From there the gown silhouette and the robe’s interior scene were worked out at full size on paper before any fabric was cut.",
        "The book doesn’t give a time period or place, so I went with a traditional hanfu gown with a dramatic flair. I made a pattern for the robe’s sleeves, then used it to draw out the Moon and Sun characters to fit.",
      ], images=[('i-008', 'Original concept art, the full bridal gown'), ('i-010', 'Full-scale figure drawing, the source for the robe scene'), ('i-009', 'Draping the neckline on the form'), ('i-011', 'Silhouette pieces cut in paper and foam')]),
      dict(title='Materials', paras=[], table=(['Component', 'Material', 'Amount'], [
        ['Gown shell', 'Iridescent color-shift spandex', '4 yd'], ['Overlay', 'Beaded ombré net and glitter mesh', '1.5 yd'], ['Underskirt', 'Pleated metallic', '1 yd'],
        ['Robe shell and lining', 'Black glittering knit and satin', '4 yd'], ['Appliqué', 'Spandex over EVA foam, rhinestone trim', '2 yd']]),
        tags=['Machine sewing', 'Foam appliqué', 'Rhinestone trim', 'Draping', 'Hand-beading'],
        images=[('i-012', 'Color-shift spandex and glitter mesh'), ('i-013', 'Iridescent overlay mesh'), ('i-014', 'Beaded ombré overlay yardage'), ('i-015', 'Beaded net, detail')]),
      dict(title='Constructing the gown', paras=[
        "The base gown was fitted on the form in the color-shift spandex, then layered with the beaded overlay. I went through a few neckline iterations before landing on the final, simpler and more traditional hanfu style. It just felt more imperial.",
        "I then made a pleated metallic underskirt over a mermaid crinoline. This was my first time using a heavily beaded fabric: I crushed the beads along the outside edge with a hammer to get a smooth, machine-sewable surface.",
      ], images=[('i-016', 'Keyhole bodice mock-up on the form'), ('i-017', 'Sweetheart bodice fitting'), ('i-018', 'Skirt panels laid out'), ('i-019', 'Gown, overlay and neckpiece, flat'), ('i-020', 'Beaded overlay with gold band'), ('i-021', 'Pleated metallic underskirt')]),
      dict(title='Building the robe scene', paras=[
        "Each figure and celestial motif was built by stretching color-shift spandex over EVA foam, outlined in rhinestone trim, and mounted to the robe’s glittering iridescent background. I glued the appliqués down with Fabri-Tac, since they’re too thick to sew.",
        "The Sun smiles with topaz jewels while the Moon cries with blue. Both bodies are filled with around 500 rhinestone crystals representing the blood of the Stars.",
      ], images=[('i-022', 'Figure pieces, rhinestone-edged'), ('i-023', 'Robed-figure reveal panels'), ('i-024', 'Banding the silhouette outline'), ('i-025', 'Spandex stretched over EVA foam, underside finished'), ('i-026', 'Stone-set motif, front'), ('i-027', 'Moon medallion, foam cut and shading'), ('i-028', 'Robe lining and bound edge')]),
      dict(title='The reveal: the blood of the Stars', paras=[
        "The robe hides the Sun and the Moon in the night on the outside. Opened, the blood of the Stars raining down from the center of the dress reveals their story.",
      ], images=[('i-029', 'Closed: the night'), ('i-000', 'Opened: the three children'), ('i-031', 'From behind: pure night'), ('i-032', 'Moon figure with blue jewels'), ('i-033', 'Sun figure with topaz jewels'), ('i-034', 'Jewel application in progress')]),
      dict(title='Accessories, wig and veil', paras=[
        "**Slippers.** A plain pair of slippers, embellished with black and purple acrylic paint and iridescent rhinestones. Small changes made a big impact.",
        "**Wig.** A simple black wig braided into low buns. In the story Maia cuts her hair short to disguise herself as a boy, since women are forbidden to tailor for the emperor. By the time she returns from her journey her hair has grown significantly, which felt right for the moment she tries the dress on in what she believes is private.",
        "**Veil.** The book describes the veil as “a piece of extra cloth”. I plan to add more jewels to the edges and contour it to my face.",
        "**Sash (dai).** Black sequin material over black canvas, with rhinestone trim and two large handmade beaded tassels.",
        "**Inner robe (moxiong).** Underneath everything is a basic black robe with long sleeves for modesty.",
      ], images=[('i-035', 'Original slippers'), ('i-036', 'Slippers after painting and jeweling'), ('i-037', 'Wig braided into low buns, with the crystal-drip veil'), ('i-038', 'Sash with beaded fringe and handmade tassels'), ('i-039', 'Inner robe (moxiong)')]),
      dict(title='Challenges', paras=[
        "**Materials.** Maia often speaks of silk, but I couldn’t justify around $400 in fabric alone. Since this hanfu is made from celestial materials, I decided satin, spandex and mesh that gave the ethereal look were fair game. It may not be correct, but I think it’s stunning, and the whole build came in around $200.",
        "**Beaded fabric.** Sewing it was brand new to me, and I didn’t like it. Smashing beads and breaking needles is not a pleasant way to work. I did it anyway, in a full face mask, slowly. Endurance is a must when bringing a story to life.",
        "**Credits.** My husband, for constantly reminding me to take pictures. My cat Meep, who masterfully kept the fabric from rolling away, and my cat Dottie, who made sure patterns were properly scattered on the floor.",
      ], images=[]),
    ]),
  dict(
    slug='snow-white', year='2024', title='Snow White: The Light Within', card='A lamp-shaped clear skirt lit from within, with a stained-glass panel for each dwarf',
    subtitle='Snow White, reimagined', event='', cover='finished',
    facts=[('Character', 'Snow White'), ('Skirt', 'Clear Worbla over a welded wire frame'), ('Lighting', '80 tea lights'), ('Panels', 'One for each of the seven dwarves')],
    intro=[
      "The Light Within is a dream-like personification of Snow White’s personality: full of love and light. She shines brightly no matter how strange or terrifying her situation is.",
      "I started from an AI rendering. AI can’t always understand the details, but it gave me a good base for where I wanted to go, and my version became far more interesting as I built what was actually in my head.",
    ],
    quote=None,
    sections=[
      dict(title='The lamp skirt', paras=[
        "This skirt was my first dive into thermoplastics (I know, ambitious). I wanted to keep the traditional princess skirt from the 1600s, gathered at the top, while giving the lamp shape a nod.",
        "I made a panel mock-up in fabric, measured the sections, then cut 10-gauge aluminum wire to size. Bending became easier once I built a wooden curve to heat the wire on. I welded the pieces together with a blowtorch (so. hot.).",
        "Then I used a heat gun to work clear TransparArt Worbla into a flowing gown shape. I learned many expensive lessons molding it, but the result was wonderful: a clear skirt.",
        "Next came the hand-cut EVA pieces. I designed each panel to feature one of the seven dwarves, with floral details and lines reminiscent of stained glass. Last, I painted the skirt with acrylic thinned with clear glue so the 80 tea lights on my homemade underskirt could shine through. I added a bow to the back and called it done.",
      ], images=[('skirt-lit', 'The finished lamp skirt, lit from inside'), ('skirt-happy', 'Happy, one of the seven stained-glass dwarf panels'), ('apple-panel.mp4', 'An apple cartouche glowing through the clear Worbla'), ('i-000', 'The AI rendering the design started from')]),
      dict(title='Corset top and sleeves', paras=[
        "I loved the off-the-shoulder look and wanted my design to be unique from the Disney version. I love 1800s femininity, so I designed the corset after that era. The apples, beading and boning trim are all handmade and hand sewn.",
        "The sleeves are TransparArt Worbla shaped over a glass pumpkin. The backgrounds are my paintings of the castle and the dwarves’ cottage, with small trees made from 3D-printer scraps and EVA, finished with white pearl and net trim.",
      ], images=[]),
      dict(title='The cape and the birds', paras=[
        "The cape hangs from two rods I bent in a vise and cut with a Sawzall, mounted on a snare drum holder, then covered in red velvet trimmed with German-style ribbon. Large buckles hidden under the faux clasps run down to the skirt to hold it in place.",
        "Last, I made the two birds that “carry” the cape: two remote-controlled cat toys as a base, with bird bodies built around them from EVA, fabric and feathers.",
      ], images=[]),
      dict(title='Shoes', paras=[
        "The shoes nod to 1600s German style. I covered them in fabric and cut holes for white fabric to pop through, added embellishments around each hole with a small blue stone between each for depth, and finished the heels with gold trim to tie the look together.",
      ], images=[('shoe-pearls', 'Velvet shoe with chiffon puffs, pearl buttons and gold rhinestone trim'), ('shoe-stones', 'The second shoe in progress, with blue stones between the puffs')]),
    ]),
  dict(
    slug='neverending-story', year='2025', title='The NeverEnding Story', card='The Childlike Empress, with Falkor and Gmork in orbit',
    subtitle='The Childlike Empress · The NeverEnding Story', event='Friday Night Costume Contest 2025', cover='image38',
    facts=[('Character', 'The Childlike Empress'), ('Source', 'The NeverEnding Story (1984)'), ('Contest', 'Friday Night Costume Contest 2025'), ('Mechanism', '3D-printed geared track, 6 V motor'), ('Rotation', 'About 45 seconds per revolution')],
    intro=[
      "When I create a cosplay for myself, I rarely choose a character in isolation. I aim to capture the whole experience, the movie, the scene and the emotions it stirs, and merge them into one wearable work of art. For me a costume isn’t just about accuracy; it’s about storytelling.",
      "The NeverEnding Story has always inspired me. As a child I was captivated not just by the adventure but by its message: imagination keeps hope alive. This cosplay is my tribute to that spirit, and to the motto I’ve carried since childhood: never stop imagining.",
    ],
    quote='How magical it would be to have Falkor and Gmork circling around me, the way the birds wrap Cinderella’s dress in ribbons.',
    sections=[
      dict(title='The spark', paras=[
        "The idea crystallized after a short clip from Cinderella, where the birds circle her and wrap her dress in ribbons. I was also inspired by the costumes of the Miss Thailand competitions, where contestants wear enormous, elaborate and even moving sculptures. I wanted that same grandeur and movement: an unforgettable display that’s as much art as costume. And it still had to fit through doorways.",
      ], images=[('image1', 'Concept drawing')]),
      dict(title='Falkor', paras=[
        "Falkor was the most challenging piece. His tall, narrow form needed a frame that would move gracefully without folding in on itself or toppling over: lightweight and extremely strong.",
        "I learned to bend PVC pipe by filling it with heated sand. Most tutorials used three-foot sections; Falkor needed nine feet. In heat-resistant gloves I taped one end, funneled in the hot sand and bent the pipe over the curve of an old barrel before it cooled.",
        "The frame was wrapped in pool noodles for bulk and packing foam to smooth the contours. His face is sculpted EVA with tiny individually shaped teeth, his eyes are ping-pong balls, his fur is soft faux fur, and his scales are over a thousand hand-laid white and iridescent sequins. A set of long false eyelashes finishes his expression.",
      ], images=[('image7', 'Sand-bent PVC spine wrapped in pool noodles'), ('image6', 'Building up the body'), ('image4', 'Sculpted EVA face with ping-pong ball eyes'), ('image5', 'Faux fur and sequin scales going on'), ('image33', 'Falkor on his mount')]),
      dict(title='Gmork', paras=[
        "Gmork was planned full size, a large imposing wolf to contrast with Falkor, built the same way with an EVA face and dark faux fur. Mounted on his rods he looked too cartoonish and overpowered the display.",
        "In the story Gmork isn’t the victor; he’s the harbinger of the Nothing. So I cut his body in half, reinforced it with a steel rod and set him lower, partly grounded. He stays menacing without taking over. Imagination and hope had to take center stage.",
      ], images=[('image8', 'Gmork taking shape'), ('image9', 'Cut down to size and set low on the base')]),
      dict(title='The Empress’s gown', paras=[
        "I wanted my own vision of what the Childlike Empress might wear: the elegance of the original with more texture and dimension, reading well up close and from across a room.",
        "The outer shell is an off-white quilt from Goodwill, its texture lifted with hand-placed backless pearls. The underlayer is a silk-like fabric with a few Swarovski crystals placed to catch the light.",
        "Around the bust and shoulders are the Southern Oracle sphinxes, the moment Atreyu’s pure heart lets him pass unharmed. I glued fabric to extra-thick interfacing, painted the figures, hand-beaded the details and boned the backs so the wings and heads stand tall. A small hand-beaded pearl crown drapes across the forehead.",
      ], images=[('image13', 'Hand-placing pearls on the quilted shell'), ('image11', 'Bodice fitting'), ('image15', 'Southern Oracle figures, painted and beaded'), ('image16', 'Beading the wings'), ('image17', 'Oracles mounted at the shoulders'), ('image14', 'Gown fitting')]),
      dict(title='The track', paras=[
        "The vision was a train-track system that would carry Falkor and Gmork around me continuously while I could still walk and move inside it. I had never built a moving mechanism, so my husband helped me learn 3D printing.",
        "We printed several iterations of the track, which works like the gears of a clock. At times success and failure were a fraction of a millimeter apart: if the pieces didn’t meet perfectly, the whole system bound up.",
        "The track sits on a circular wooden base with the center cut out so I can stand inside it. A small 6 V motor drives it, and eight ball-bearing rollers underneath keep the motion smooth.",
      ], images=[('image21', 'Laying out the printed track'), ('image20', 'Track sections'), ('image22', '3D-printed gear and motor mount'), ('image19', 'Ball-bearing roller'), ('image23', 'Assembling the base'), ('image24', 'First stand-in test')]),
      dict(title='The world around her', paras=[
        "The base connects to a 10-gauge wire frame I welded myself. Around the moving top I added EVA foam, sculpted mountains and valleys from spray foam, shaped them with a sander (gloves and mask on), and painted mottled layers to match Fantasia.",
        "Then the characters: Teeny Weeny and his racing snail, the Rock Biter, Night Hob and his bat, Atreyu and Artax, Morla, and of course Bastian, each painted to match the film. The frame became a living diorama: a world in motion, worn like a crown of memories.",
      ], images=[('image25', 'Shaping the spray-foam terrain'), ('image26', 'Mountains before paint'), ('image29', 'Character cut-outs before painting'), ('image27', 'Night Hob and his bat'), ('image31', 'Teeny Weeny and his racing snail'), ('image30', 'The Rock Biter'), ('image28', 'Atreyu and Artax'), ('image32', 'Bastian')]),
      dict(title='Assembly and reveal', paras=[
        "Final assembly was the most stressful step: omnidirectional wheels on the base, the printed motor mounts and gears pushed in until they meshed, then glued and bolted. The motor runs from a 6 V battery; one revolution takes about 45 seconds. The dress frame bolts to the base, the background mounts to the track, and Gmork and Falkor slide onto their rod.",
        "Finally I step inside, drop the skirt over the structure and become the Childlike Empress, with the mechanics hidden beneath. A mechanical, electrical build wrapped in cosplay magic: a mixed-media tribute to a mixed-media movie, and a reminder to keep imagination alive.",
      ], images=[('image35', 'Final assembly'), ('image36', 'The finished base'), ('image37', 'Motor and battery underneath'), ('image38', 'Finished'), ('image39', 'In motion'), ('image40', 'Falkor and Gmork in orbit'), ('falkor-orbit.mp4', 'Falkor circling, lit by the glowing Auryn'), ('convention-falkor-gmork', 'At Dragon Con 2025, with Gmork at her feet and Bastian painted on the base'), ('gown-convention', 'The Southern Oracle shoulders and quilted pearl gown')]),
    ]),
  dict(
    slug='bunny-the-clown', year='2026', title='Bunny the Clown', card='Buggy the Clown from One Piece, bunny style',
    subtitle='Buggy the Clown · One Piece', event='', cover='front',
    facts=[('Character', 'Buggy the Clown'), ('Source', 'One Piece'), ('Year', '2026')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('front', 'Knife-fingered gloves, striped corset and treasure-chest purse'), ('pose', 'The cape, fur collar and boots'), ('convention-wide', 'At the convention')])]),
  dict(
    slug='creaturess-from-the-black-lagoon', year='2026', title='Creaturess from the Black Lagoon', card='The Creature from the Black Lagoon, reimagined as a scaled gown',
    subtitle='The Creature from the Black Lagoon, reimagined', event='', cover='front',
    facts=[('Character', 'The Creature from the Black Lagoon'), ('Year', '2026')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('front', 'Layered scales, gold breastplate and kelp-trimmed hem'), ('pose', 'Feathered headpiece and webbed gloves')])]),
  dict(
    slug='beetlejuice', year='2024', title='Beetlejuice', card='Beetlejuice, bunny style, from the floor to the Dragon Con stage',
    subtitle='Beetlejuice', event='', cover='convention',
    facts=[('Character', 'Beetlejuice'), ('Year', '2024')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('convention', 'Striped corset, sandworm ears and glitter-green heels'), ('stage', 'On the Dragon Con stage')])]),
]

NICK = [
  dict(
    slug='vidar', year='2026', title='Vidar', card='The Silent God of Vengeance, with motion-driven lighting',
    subtitle='Vidar, Norse god of vengeance', event='Friday Night Costume Contest · Novice', cover='finished',
    facts=[('Source art', 'Sam Flegal, Fateful Signs (with the artist’s permission)'), ('Design goal', 'Every lighting effect driven by motion. No switches on stage.'), ('Build time', 'About 350 hours over nine months'), ('Cost', 'Just under $200, plus about $150 in prototyping'), ('Fabrication', 'ABS printing and vapor smoothing, EVA thermoforming, laser cutting, resin, soft goods, LED wiring'), ('Software', '3D scanning, Blender, Autodesk Fusion, C++ on Arduino')],
    intro=[
      "I found Vidar in the Dragon Con vendor hall in 2025, in a painting by Sam Flegal of Fateful Signs. Vidar is the silent son of Odin, the one who survives Ragnarök and avenges his father. Flegal gave him a heavy forged-stone body with fire running through the seams, and I kept walking back to the booth to look at it.",
      "I work backwards when I pick a costume: I decide what I want to learn to build, then find a character who gives me an excuse to build it. I’d been reading about accelerometer-driven LEDs for months. So I set one rule: no buttons. Every effect had to answer to something physical: how hard I hit the floor, how I’m holding the sword, or what kind of light is in the room.",
    ],
    quote='Step hard and more of the leg lights up. Stand still and it settles back to a low ember.',
    sections=[
      dict(title='On stage', paras=[], images=[('stage', 'On stage. Photo © Badger Studios')]),
      dict(title='How each piece responds', paras=[
        "Three of the seven effects use no electronics at all. That was deliberate: every powered effect is one more battery to charge, one more connector to seat while dressing, and one more solder joint that can break mid-performance.",
      ], table=(['Piece', 'What it does', 'What triggers it'], [
        ['Greaves', 'A column of light climbs the leg and fades back down', 'Accelerometer at the heel reading foot-strike force'],
        ['Sword', 'Color and intensity shift as the blade comes up', 'IMU in the hilt tracking blade elevation'],
        ['Shield', 'Runes glow in the dark; UV flare under blacklight; LEDs in light', 'Passive glow pigment under UV resin, plus flickering LEDs'],
        ['Collar', 'Warm gradient thrown up onto the jaw and mask', 'Constant-current LEDs through hand-painted cellophane'],
        ['Pauldrons', 'Eye sockets glow in a dim room', 'Passive glow pigment, no power'],
        ['Bracers', 'Look internally lit, and aren’t', 'Painted highlights over reflective gold fabric'],
        ['Helmet', 'Flames move and flicker', 'Micro-LEDs and a 5 V fan stirring cellophane flames']]), images=[]),
      dict(title='Greaves and leg lighting', paras=[
        "The legs carry most of the lighting, and the whole costume was designed around them. The greaves are body-molded thermoformed EVA with metallic gold fabric stretched over the inner structure and EVA plating on top.",
        "The gold isn’t just decoration: it’s a continuous reflector. The LED strands point inward at it, so light bounces and spreads instead of showing as a row of dots. That change did more for how the legs look than anything else I tried, and it cost about $12 in fabric.",
        "The back of each greave hides a printed enclosure that reads as armor outside and works as a junction box inside: battery, microcontroller and wiring, with the Arduino reachable for tweaks. Two addressable RGB strands per leg are driven by an MPU6050 accelerometer reading vertical G-force on each step.",
        "The firmware is a little over 500 lines of C++, with every tuning value as a named constant at the top of the file. Attack, hold and decay are borrowed from audio envelopes: a fast attack with a slow decay makes a step read as an impact, then lets the flame fade away.",
        "**What went wrong.** My first connectors were for 10 mm strands, not 8 mm. Fine on the bench, but bent into position they lost continuity. I spent a week rerunning wires and cutting open foam, only to find I’d used the connectors meant for my under-cabinet lights.",
      ], images=[('image2', 'Dual LED strands laid into the greave, following penciled layout lines'), ('image3', 'Rear junction box with the Nano, breadboard and wiring'), ('image4', 'Foam covering laid out during glue-up'), ('image5', 'The greave shell mid-build'), ('image6', 'Working schematic for the greave circuit'), ('image7', 'Firmware with every value as a named constant')]),
      dict(title='Sword', paras=[
        "Vidar is the second strongest of the Norse gods, after Thor, so the sword had to hold its own next to a Mjölnir from the back of the ballroom. It weighs 6 lb: a 4 lb blade balanced by a 2 lb pommel that pulls the center of mass back to my hand.",
        "Blade, cavity, hilt and pommel were modeled from scratch in Blender. Twin dowel channels run through the blade, hilt and pommel and carry the load; without them a printed blade this long shears at the guard on the first real swing. It’s printed in ABS with a clear PETG core, and the Elder Futhark runes spell “vengeance”.",
        "The guard began as a demon skull I split, mirrored and hollowed. It houses the microcontroller, orientation sensor and power, and lights the eye sockets from inside. As the blade rotates toward vertical, the light grows up the blade and brightens, following my movement live.",
      ], images=[('image10', 'Blade modeled from scratch in Blender'), ('image11', 'Hilt electronics cavity, dowel spine visible'), ('image12', 'Hand-drawn sword schematic'), ('image13', 'The finished blade, lit')]),
      dict(title='Shield', paras=[
        "Two feet across: any bigger and it covers the armor on stage and competes with the sword. (Also, foam board comes in 2 × 2 ft squares.) The core is high-density foam board, cut and grooved into planks and hand-scraped for grain, with six printed edge pieces for a proper Viking rim.",
        "The laser etch was the most nerve-wracking stretch of the build. The shield is wider than the laser bed, so it went through in two angled passes with one shot to get it right. Then I deepened the channels with a soldering iron, melting foam on purpose, slowly, with ventilation and a respirator.",
        "Each channel has red glow paint under clear UV-reactive resin, so it reads three ways: red in room light, a UV flare under blacklight, and only the runes glowing in full dark. The hub is a printed horned skull; one horn passes through the face to become the forearm support and grip. It’s my favorite mechanic in the whole costume.",
        "**What I’d redo.** The resin leaked out of the channel ends before I could get the disc to the UV lamp. Next time I’ll seal the ends first and cure outside in the sun.",
      ], images=[('image14', 'Foam board core, cut for the skull hub'), ('image15', 'Opening the rune channels with a soldering iron, under a respirator'), ('image16', 'The shield in daylight'), ('image17', 'The shield in the dark'), ('image18', 'Painted skull and horn')]),
      dict(title='Helmet and face shield', paras=[
        "No chin strap. The helmet holds by friction alone, which only works because it was modeled against a 3D scan of my own head. The face guard comes off independently, so I can pull it on stage to reveal a sealed mouth for the silent god.",
        "Micro-LEDs line the crown next to a small 5 V fan. The fan cools nothing: it moves air across cellophane flames so they shift and lift. Light alone gives a static glow; the airflow sells it as fire, and it’s the cheapest part of the build.",
      ], images=[('image19', 'Crown and face sculpt in Blender, against a scan of my head'), ('image20', 'Test-fitting the crown band and printed face shield'), ('image21', 'Painted crown and flames')]),
      dict(title='Pauldrons', paras=[
        "Printed in ABS from heavily modified demon-skull models, reshaped wider and heavier, then vapor-smoothed to melt away the print lines.",
        "They float. Magnets inside each pauldron meet magnets held to my skin with kinesiology tape: no harness, no strap across the chest. I can raise both arms overhead and they stay put, and I can wear them higher for physique display or lower for a more armored look. The eye sockets are glow paint, with no power or wiring.",
      ], images=[('image22', 'Crown and pauldron fit check'), ('image23', 'A pauldron after vapor smoothing'), ('image24', 'Glow pigment in the eye sockets')]),
      dict(title='Bracers, collar and boots', paras=[
        "**Bracers.** Structural EVA wrapped in the same gold fabric as the legs, painted with high-contrast shading and forced highlights so they look lit. There’s nothing electronic in them; elastic inside holds them to the forearm.",
        "**Collar.** An EVA frame carrying layered cellophane hand-painted with translucent acrylics, so the light builds a gradient. A constant-current LED strip at the back throws light up onto the jaw and mask.",
        "**Boots.** Built last, on purpose, once I knew exactly where the greaves would sit. The EVA cladding is thermoformed at an angle into a landing ridge that the greave drops onto and locks, which stops the armor slipping down the calf. Then I found I couldn’t get my foot in, so the ankle build-up moved onto the greave with its own Velcro closure.",
      ], images=[('image25', 'Inside the bracer: EVA frame and elastic'), ('image26', 'Painted and unpainted bracers'), ('image27', 'Collar, before painting')]),
      dict(title='Power and getting dressed', paras=[
        "Every active effect runs on its own pack, so a dead battery costs one effect, not the costume. Every housing can be charged without opening it, a requirement for charging everything overnight in a hotel room between shows.",
      ], steps=[
        'Charge check and skin prep: kinesiology tape and magnet pads on both shoulders.',
        'Step into the waist piece and leggings; secure the thigh armor.',
        'Power on the greaves, fasten them, step into the boots and seat the greaves on the landing ridge.',
        'Power on the collar, attach the pauldrons magnetically, drop the collar over the neck.',
        'Fit the face guard, then the crown; power the crown LEDs and start the flame fan.',
        'Power on the sword and shield, and check the sword responds to rotation.',
      ], images=[]),
    ]),
  dict(
    slug='mr-clean', year='2024', title='Mr. Clean', card='Spotless whites, bright brows, mop at the ready',
    subtitle='Mr. Clean', event='', cover='front',
    facts=[('Character', 'Mr. Clean'), ('Year', '2024')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('front', 'Arms crossed, mop at the ready')])]),
  dict(
    slug='rocketeer', year='2024', title='Rocketeer', card='Gold helmet, bomber jacket and twin-rocket jet pack',
    subtitle='The Rocketeer', event='', cover='front',
    facts=[('Character', 'The Rocketeer'), ('Year', '2024')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('front', 'Helmet, jacket and Mauser'), ('jetpack', 'The twin-rocket jet pack')])]),
  dict(
    slug='spartan-warrior', year='2026', title='Spartan Warrior', card='Bronze helmet, shield and spear, marching with the phalanx',
    subtitle='Spartan Warrior', event='', cover='parade',
    facts=[('Character', 'Spartan warrior')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('parade', 'Marching in the parade'), ('profile', 'Helmet, shield and spear')])]),
  dict(
    slug='turok-dinosaur-hunter', year='2024', title='Turok Dinosaur Hunter', card='Beaded breastplate, flint spear and a stack of trophy raptors',
    subtitle='Turok Dinosaur Hunter', event='', cover='front',
    facts=[('Character', 'Turok')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('front', 'Spear stacked with raptor heads'), ('with-carrie', 'With Carrie')])]),
  dict(
    slug='duffman', year='2026', title='Duffman', card='Oh yeah. Cape, cans and a well-earned rest',
    subtitle='Duffman', event='', cover='convention',
    facts=[('Character', 'Duffman'), ('Source', 'The Simpsons')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('convention', 'Oh yeah! Cape, cap and a belt of Duff'), ('cans', 'Can in hand, shades on'), ('front', 'Off duty')])]),
  dict(
    slug='halloween-masquerade', year='2026', title='Halloween Masquerade', card='Metal masks, a brocade vest and a war hammer',
    subtitle='Halloween Masquerade', event='', cover='mask-night',
    facts=[('Occasion', 'Halloween masquerade')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('mask-night', 'Mask and war hammer'), ('mask-day', 'Filigree mask and brocade vest')])]),
  dict(
    slug='denton-van-zan', year='2025', title='Denton Van Zan', card='The dragon slayer from Reign of Fire, axe in hand',
    subtitle='Denton Van Zan · Reign of Fire', event='', cover='axe',
    facts=[('Character', 'Denton Van Zan'), ('Source', 'Reign of Fire (2002)')],
    intro=[], quote=None,
    sections=[dict(title='Photos', paras=[], images=[('axe', 'Shearling vest, ammo belt and the dragon-hunting axe'), ('mirror', 'Fitting check: tattoos and fatigues')])]),
]
