INSERT INTO "pois" (
  "id",
  "name",
  "lat",
  "lng",
  "description",
  "tags",
  "media",
  "type",
  "is_deleted",
  "created_at",
  "updated_at"
) VALUES
(2, '🐊 Honey Island Swamp', 30.2156, -89.5528,
 'Pantano con mayor densidad de caimanes de Luisiana',
 '["caiman","swamp","wildlife","bayou"]',
 '[{"url":"https://images.unsplash.com/photo-1630097594830-52abbccbaaeb?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","type":"image","title":"Portada"}]',
 'wildlife_area', false, '2026-02-09 11:00:00+00', '2026-02-09 11:00:00+00'),

(3, '🌳 Live Oak Plantation', 30.0642, -90.8836,
 'Plantación con robles centenarios del sur profundo',
 '["plantation","oak_tree","history","civil_war"]',
 '[{"url":"https://images.unsplash.com/photo-1652118318955-dd7aa7f96f31?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","type":"image","title":"Portada"}]',
 'plantation', false, '2026-02-09 12:00:00+00', '2026-02-09 12:00:00+00'),

(1, '🏚️ Jean Lafitte''s Blacksmith Shop', 29.9584, -90.0592,
 'Taberna más antigua de USA (1722) - escondite de piratas',
 '["pirata","historia","taberna","french_quarter"]',
 '[{"url":"https://images.unsplash.com/photo-1484271710659-125d48c9fad6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","type":"image","title":"Portada"}]',
 'historical_building', false, '2026-02-09 10:00:00+00', '2026-02-09 10:00:00+00'),

(4, '🎻 Cajun Music Hall', 30.451, -92.3028,
 'Corazón musical cajún - zydeco y fiddles',
 '["cajun","zydeco","music","dance"]',
 '[{"url":"https://images.unsplash.com/photo-1702690401395-767fe2cdf3a7?q=80&w=1174&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","type":"image","title":"Portada"}]',
 'cultural_center', false, '2026-02-09 13:00:00+00', '2026-02-09 13:00:00+00'),

(5, '🦪 Grand Isle Tarpons', 29.2058, -90.0003,
 'Pesca de tarpon en el Golfo - paraíso pesquero',
 '["fishing","tarpon","gulf","beach"]',
 '[{"url":"https://images.unsplash.com/photo-1597179874248-905a95903827?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","type":"image","title":"Portada"}]',
 'fishing_spot', false, '2026-02-09 14:00:00+00', '2026-02-09 14:00:00+00');


INSERT INTO "routes" (
  "id",
  "name",
  "description",
  "poi_ids",
  "is_deleted",
  "created_at",
  "updated_at",
  "image_url"
) VALUES
(1, '🏚️⚜️🛶 Bayou Pirate Adventure',
 'French Quarter → Plantaciones → Caimanes reales',
 '[1,10,6,2]',
 false,
 '2026-02-12 16:59:16.009131+00',
 '2026-02-15 14:38:16.943642+00',
 'https://images.unsplash.com/photo-1767111385226-58a85f121ca0?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

(2, '🌳🏛️🔥 Creole Deep South',
 'Oak Alley → Laura → Tabasco Factory → Cajun music',
 '[11,12,15,16,4]',
 false,
 '2026-02-12 16:59:16.009131+00',
 '2026-02-15 14:39:03.556672+00',
 'https://images.unsplash.com/photo-1673037287921-f46ca586c939?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

(3, '🐊🦪🌊 Louisiana Gulf Extreme',
 'Honey Island → Grand Isle → Port Fourchon fishing',
 '[2,17,18,5]',
 false,
 '2026-02-12 16:59:16.009131+00',
 '2026-02-15 14:40:54.62867+00',
 'https://images.unsplash.com/photo-1592947419095-4a2b4bde9161?q=80&w=731&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

(4, '🌶️🍤🎻 Cajun Food & Zydeco',
 'Tabasco → Boudin stops → Cajun music explosion',
 '[15,19,20,4]',
 false,
 '2026-02-12 16:59:16.009131+00',
 '2026-02-15 14:42:56.773197+00',
 'https://plus.unsplash.com/premium_photo-1707581577440-d258dbb0120c?q=80&w=688&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');