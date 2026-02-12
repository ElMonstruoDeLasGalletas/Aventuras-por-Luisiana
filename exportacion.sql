INSERT INTO pois (name, lat, lng, description, tags, media, type, is_deleted, created_at, updated_at) VALUES
('🏚️ Jean Lafitte''s Blacksmith Shop', 29.9584, -90.0592, 'Taberna más antigua de USA (1722) - escondite de piratas', '["pirata","historia","taberna","french_quarter"]'::jsonb, '[{"type":"image","url":"/media/jean_lafitte.jpg","title":"Taberna 1722"},{"type":"audio","url":"/media/pirate_song.mp3"}]'::jsonb, 'historical_building', false, '2026-02-09 10:00:00', '2026-02-09 10:00:00'),
('🐊 Honey Island Swamp', 30.2156, -89.5528, 'Pantano con mayor densidad de caimanes de Luisiana', '["caiman","swamp","wildlife","bayou"]'::jsonb, '[{"type":"video","url":"/media/honey_island.mp4","title":"Paseo en barca"},{"type":"image","url":"/media/alligator.jpg"}]'::jsonb, 'wildlife_area', false, '2026-02-09 11:00:00', '2026-02-09 11:00:00'),
('🌳 Live Oak Plantation', 30.0642, -90.8836, 'Plantación con robles centenarios del sur profundo', '["plantation","oak_tree","history","civil_war"]'::jsonb, '[{"type":"image","url":"/media/live_oak.jpg","title":"Robles 300 años"},{"type":"image","url":"/media/plantation_house.jpg"}]'::jsonb, 'plantation', false, '2026-02-09 12:00:00', '2026-02-09 12:00:00'),
('🎻 Cajun Music Hall', 30.4510, -92.3028, 'Corazón musical cajún - zydeco y fiddles', '["cajun","zydeco","music","dance"]'::jsonb, '[{"type":"video","url":"/media/cajun_dance.mp4","title":"Baile zydeco"},{"type":"audio","url":"/media/fiddle_tune.mp3"}]'::jsonb, 'cultural_center', false, '2026-02-09 13:00:00', '2026-02-09 13:00:00'),
('🦪 Grand Isle Tarpons', 29.2058, -90.0003, 'Pesca de tarpon en el Golfo - paraíso pesquero', '["fishing","tarpon","gulf","beach"]'::jsonb, '[{"type":"image","url":"/media/tarpon_fishing.jpg","title":"Tarpon 100lb"},{"type":"video","url":"/media/gulf_waves.mp4"}]'::jsonb, 'fishing_spot', false, '2026-02-09 14:00:00', '2026-02-09 14:00:00');

-- 🔥 FRENCH QUARTER (Nueva Orleans)
('⚜️ Jackson Square', 29.9578, -90.0634, 'Corazón del French Quarter - artistas y músicos callejeros', '["french_quarter","music","art"]'::jsonb, '[{"type":"image","url":"/media/jackson_square.jpg"}]'::jsonb, 'square', false, NOW(), NOW()),
('🍹 Pat O''Brien''s', 29.9581, -90.0608, 'Creadores del Hurricane - cóctel oficial de Mardi Gras', '["cocktail","mardi_gras","bar"]'::jsonb, '[{"type":"image","url":"/media/hurricane_cocktail.jpg"}]'::jsonb, 'bar', false, NOW(), NOW()),
('🎺 Preservation Hall', 29.9577, -90.0643, 'Jazz tradicional desde 1961 - NO te lo pierdas', '["jazz","music","live"]'::jsonb, '[{"type":"audio","url":"/media/preservation_jazz.mp3"}]'::jsonb, 'music_venue', false, NOW(), NOW()),

-- 🔥 PLANTACIONES
('🏛️ Oak Alley Plantation', 30.0047, -90.7752, 'Túnel de 300 robles - LA plantación más fotografiada', '["plantation","oaks","iconic"]'::jsonb, '[{"type":"image","url":"/media/oak_alley.jpg"}]'::jsonb, 'plantation', false, NOW(), NOW()),
('💀 Laura Plantation', 29.9975, -90.7758, 'Historias reales de esclavos - cuentos Br’er Rabbit', '["slavery","folklore","creole"]'::jsonb, '[{"type":"image","url":"/media/laura_plantation.jpg"}]'::jsonb, 'plantation', false, NOW(), NOW()),

-- 🔥 BAYOUS & SWAMPS
('🛶 Barataria Preserve', 29.7322, -90.1167, 'Senderos boardwalk + caimanes - Jean Lafitte National Park', '["swamp","hiking","alligators"]'::jsonb, '[{"type":"image","url":"/media/barataria_boardwalk.jpg"}]'::jsonb, 'nature_reserve', false, NOW(), NOW()),
('🎣 Manchac Swamp', 30.2997, -90.5497, 'Pescadores cajún + airboats - swamp life real', '["fishing","airboat","cajun"]'::jsonb, '[{"type":"video","url":"/media/manchac_airboat.mp4"}]'::jsonb, 'swamp', false, NOW(), NOW()),

-- 🔥 CAJÚN COUNTRY
('🔥 Tabasco Factory', 29.9500, -91.4067, 'Salsa TABASCO original - tour + degustación picante', '["tabasco","factory","food"]'::jsonb, '[{"type":"image","url":"/media/tabasco_factory.jpg"}]'::jsonb, 'factory', false, NOW(), NOW()),
('🐟 Avery Island Jungle Garden', 29.9025, -91.3969, 'Egrets + bambúes exóticos - jardín japonés', '["garden","birds","jungle"]'::jsonb, '[{"type":"image","url":"/media/avery_island.jpg"}]'::jsonb, 'garden', false, NOW(), NOW()),

-- 🔥 GULF COAST
('🏖️ Grand Isle State Park', 29.2094, -89.9942, 'Playas + pesca tarpon - gateway al Golfo', '["beach","fishing","gulf"]'::jsonb, '[{"type":"image","url":"/media/grand_isle_beach.jpg"}]'::jsonb, 'beach', false, NOW(), NOW()),
('🪝 Port Fourchon', 29.1075, -90.1042, 'Puerto pesquero + rigs petroleros - working coast', '["fishing","oil","port"]'::jsonb, '[{"type":"image","url":"/media/port_fourchon.jpg"}]'::jsonb, 'port', false, NOW(), NOW()),

-- 🔥 MUSIC & FOOD
('🌶️ Prejean''s Restaurant', 30.2236, -92.0639, 'Crawfish étouffée + alligator - biblia cajún', '["cajun_food","crawfish","restaurant"]'::jsonb, '[{"type":"image","url":"/media/prejeans_crawfish.jpg"}]'::jsonb, 'restaurant', false, NOW(), NOW()),
('🍤 Boudin Trail Stop', 30.1228, -92.1497, 'Boudin cajún auténtico - embutido de arroz + hígado', '["boudin","food","cajun"]'::jsonb, '[{"type":"image","url":"/media/boudin_trail.jpg"}]'::jsonb, 'food_stop', false, NOW(), NOW());


-- 🛤️ RUTAS COMPLETAS con POIs intermedios
INSERT INTO routes (name, description, poi_ids, is_deleted, created_at, updated_at) VALUES
-- Ruta 1: French Quarter → Swamps (5 POIs)
('🏚️⚜️🛶 Bayou Pirate Adventure', 
 'French Quarter → Plantaciones → Caimanes reales', 
 '[1,10,6,2]'::jsonb, false, NOW(), NOW()),

-- Ruta 2: Plantations → Cajun Country (6 POIs)  
('🌳🏛️🔥 Creole Deep South', 
 'Oak Alley → Laura → Tabasco Factory → Cajun music', 
 '[11,12,15,16,4]'::jsonb, false, NOW(), NOW()),

-- Ruta 3: Ultimate Gulf Coast (5 POIs)
('🐊🦪🌊 Louisiana Gulf Extreme', 
 'Honey Island → Grand Isle → Port Fourchon fishing', 
 '[2,17,18,5]'::jsonb, false, NOW(), NOW()),

-- Ruta 4: Foodie Cajun Trail (4 POIs)
('🌶️🍤🎻 Cajun Food & Zydeco', 
 'Tabasco → Boudin stops → Cajun music explosion', 
 '[15,19,20,4]'::jsonb, false, NOW(), NOW());

INSERT INTO tags (name, created_at) VALUES
('pirata', NOW()),
('historia', NOW()),
('taberna', NOW()),
('french_quarter', NOW()),
('caiman', NOW()),
('swamp', NOW()),
('wildlife', NOW()),
('bayou', NOW()),
('plantation', NOW()),
('oak_tree', NOW()),
('history', NOW()),
('civil_war', NOW()),
('cajun', NOW()),
('zydeco', NOW()),
('music', NOW()),
('dance', NOW()),
('fishing', NOW()),
('tarpon', NOW()),
('gulf', NOW()),
('beach', NOW()),
('art', NOW()),
('cocktail', NOW()),
('mardi_gras', NOW()),
('bar', NOW()),
('jazz', NOW()),
('live', NOW()),
('oaks', NOW()),
('iconic', NOW()),
('slavery', NOW()),
('folklore', NOW()),
('creole', NOW()),
('hiking', NOW()),
('alligators', NOW()),
('airboat', NOW()),
('tabasco', NOW()),
('factory', NOW()),
('food', NOW()),
('garden', NOW()),
('birds', NOW()),
('jungle', NOW());
