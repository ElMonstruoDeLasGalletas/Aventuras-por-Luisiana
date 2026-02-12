-- Adminer 5.4.1 PostgreSQL 16.11 dump

DROP TABLE IF EXISTS "pois";
DROP SEQUENCE IF EXISTS pois_id_seq;
CREATE SEQUENCE pois_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pois" (
    "id" integer DEFAULT nextval('pois_id_seq') NOT NULL,
    "name" character varying(200) NOT NULL,
    "lat" double precision NOT NULL,
    "lng" double precision NOT NULL,
    "description" character varying,
    "tags" jsonb NOT NULL,
    "media" jsonb NOT NULL,
    "type" character varying(60),
    "is_deleted" boolean NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "pois_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX ix_pois_name ON public.pois USING btree (name);

CREATE INDEX ix_pois_type ON public.pois USING btree (type);


DROP TABLE IF EXISTS "reviews";
DROP SEQUENCE IF EXISTS reviews_id_seq;
CREATE SEQUENCE reviews_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."reviews" (
    "id" integer DEFAULT nextval('reviews_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "route_id" integer NOT NULL,
    "rating" integer NOT NULL,
    "content" character varying(1000),
    "is_deleted" boolean NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "reviews_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "rating_range" CHECK (((rating >= 1) AND (rating <= 5)))
)
WITH (oids = false);

CREATE UNIQUE INDEX uq_user_poi_review ON public.reviews USING btree (user_id, route_id);

CREATE INDEX ix_reviews_route_id ON public.reviews USING btree (route_id);

CREATE INDEX ix_reviews_rating ON public.reviews USING btree (rating);

CREATE INDEX ix_reviews_user_id ON public.reviews USING btree (user_id);


DROP TABLE IF EXISTS "roles";
DROP SEQUENCE IF EXISTS roles_id_seq;
CREATE SEQUENCE roles_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."roles" (
    "id" integer DEFAULT nextval('roles_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    CONSTRAINT "roles_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX roles_name_key ON public.roles USING btree (name);


DROP TABLE IF EXISTS "routes";
DROP SEQUENCE IF EXISTS routes_id_seq;
CREATE SEQUENCE routes_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."routes" (
    "id" integer DEFAULT nextval('routes_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    "description" character varying,
    "poi_ids" jsonb NOT NULL,
    "is_deleted" boolean NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "routes_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


DROP TABLE IF EXISTS "tags";
DROP SEQUENCE IF EXISTS tags_id_seq;
CREATE SEQUENCE tags_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tags" (
    "id" integer DEFAULT nextval('tags_id_seq') NOT NULL,
    "name" character varying(50) NOT NULL,
    "created_at" timestamptz NOT NULL,
    CONSTRAINT "tags_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX ix_tags_name ON public.tags USING btree (name);


DROP TABLE IF EXISTS "user_favs";
DROP SEQUENCE IF EXISTS user_favs_id_seq;
CREATE SEQUENCE user_favs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_favs" (
    "id" integer DEFAULT nextval('user_favs_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "route_id" integer NOT NULL,
    "created_at" timestamptz NOT NULL,
    CONSTRAINT "user_favs_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX uq_user_route ON public.user_favs USING btree (user_id, route_id);

CREATE INDEX ix_user_favs_route_id ON public.user_favs USING btree (route_id);

CREATE INDEX ix_user_favs_user_id ON public.user_favs USING btree (user_id);


DROP TABLE IF EXISTS "user_preferences";
DROP SEQUENCE IF EXISTS user_preferences_id_seq;
CREATE SEQUENCE user_preferences_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_preferences" (
    "id" integer DEFAULT nextval('user_preferences_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "user_preferences_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX ix_user_preferences_user_id ON public.user_preferences USING btree (user_id);


DROP TABLE IF EXISTS "user_preferred_tags";
DROP SEQUENCE IF EXISTS user_preferred_tags_id_seq;
CREATE SEQUENCE user_preferred_tags_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_preferred_tags" (
    "id" integer DEFAULT nextval('user_preferred_tags_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "tag_id" integer NOT NULL,
    "created_at" timestamptz NOT NULL,
    CONSTRAINT "user_preferred_tags_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX uq_user_tag ON public.user_preferred_tags USING btree (user_id, tag_id);

CREATE INDEX ix_user_preferred_tags_tag_id ON public.user_preferred_tags USING btree (tag_id);

CREATE INDEX ix_user_preferred_tags_user_id ON public.user_preferred_tags USING btree (user_id);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "email" character varying(255) NOT NULL,
    "name" character varying(120) NOT NULL,
    "password_hash" character varying(255) NOT NULL,
    "created_at" timestamptz NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);

INSERT INTO "users" ("id", "email", "name", "password_hash", "created_at") VALUES
(1,	'user@example.com',	'string',	'$2b$12$IIyfvFmAVtHynPrc53r1PuEoZnY5bq94Hrrfjmn4VlN55LEGwG3Qa',	'2026-02-09 17:06:25.580014+00');

ALTER TABLE ONLY "public"."reviews" ADD CONSTRAINT "reviews_route_id_fkey" FOREIGN KEY (route_id) REFERENCES routes(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."reviews" ADD CONSTRAINT "reviews_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."user_favs" ADD CONSTRAINT "user_favs_route_id_fkey" FOREIGN KEY (route_id) REFERENCES routes(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."user_favs" ADD CONSTRAINT "user_favs_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."user_preferences" ADD CONSTRAINT "user_preferences_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."user_preferred_tags" ADD CONSTRAINT "user_preferred_tags_tag_id_fkey" FOREIGN KEY (tag_id) REFERENCES tags(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."user_preferred_tags" ADD CONSTRAINT "user_preferred_tags_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

-- 2026-02-11 17:36:31 UTC