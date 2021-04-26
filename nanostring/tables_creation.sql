BEGIN;
--
-- Create model Category
--
CREATE TABLE "data_category" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(100) NOT NULL UNIQUE, "description" varchar(125) NULL);
--
-- Create model Disease2BScanVectorized
--
CREATE TABLE "data_disease2bscanvectorized" ("id" serial NOT NULL PRIMARY KEY, "fid" bigint NOT NULL, "dn" bigint NOT NULL, "name" varchar(254) NULL, "geom" geometry(MULTIPOLYGON,3857) NOT NULL);
--
-- Create model Normal2BScanVectorized
--
CREATE TABLE "data_normal2bscanvectorized" ("id" serial NOT NULL PRIMARY KEY, "fid" bigint NOT NULL, "dn" bigint NOT NULL, "name" varchar(254) NULL, "geom" geometry(MULTIPOLYGON,3857) NOT NULL);
--
-- Create model RawCSVFiles
--
CREATE TABLE "data_rawcsvfiles" ("id" serial NOT NULL PRIMARY KEY, "file_name" varchar(125) NOT NULL, "file" varchar(100) NOT NULL, "category_id" integer NULL);
--
-- Create model Kidney_Sample_Annotations
--
CREATE TABLE "data_kidney_sample_annotations" ("id" serial NOT NULL PRIMARY KEY, "slide_name" varchar(25) NULL, "scan_name" varchar(50) NULL, "roi_label" smallint NULL CHECK ("roi_label" >= 0), "segment_label" varchar(125) NULL, "segment_display_name" varchar(250) NULL, "sample_id" varchar(125) NULL, "aoi_surface_area" double precision NULL, "aoi_nuclei_count" smallint NULL CHECK ("aoi_nuclei_count" >= 0), "roi_coordinate_x" integer NULL, "roi_coordinate_y" integer NULL, "raw_reads" integer NULL, "trimmed_reads" integer NULL, "stitched_reads" integer NULL, "aligned_reads" integer NULL, "duplicated_reads" integer NULL, "sequencing_saturation" double precision NULL, "umiq_30" double precision NULL, "rtsq_30" double precision NULL, "disease_status" varchar(25) NULL, "pathology" varchar(25) NULL, "region" varchar(25) NULL, "loq" double precision NULL, "normalization_factor" double precision NULL, "geom" geometry(POINT,3857) NULL, "category_id" integer NULL);
--
-- Create model Cell_Types_for_Spatial_Decon
--
CREATE TABLE "data_cell_types_for_spatial_decon" ("id" serial NOT NULL PRIMARY KEY, "cluster_id" varchar(8) NULL, "alias" varchar(8) NULL, "data_set" varchar(250) NULL, "number_of_cells" smallint NULL CHECK ("number_of_cells" >= 0), "cell_type1" varchar(125) NULL, "cell_type2" varchar(125) NULL, "cell_type3" varchar(125) NULL, "cell_type_specific" varchar(125) NULL, "cell_type_general" varchar(125) NULL, "cluster_name" varchar(125) NULL, "category_id" integer NULL);
CREATE INDEX "data_category_name_24e751a3_like" ON "data_category" ("name" varchar_pattern_ops);
CREATE INDEX "data_disease2bscanvectorized_geom_id" ON "data_disease2bscanvectorized" USING GIST ("geom");
CREATE INDEX "data_normal2bscanvectorized_geom_id" ON "data_normal2bscanvectorized" USING GIST ("geom");
ALTER TABLE "data_rawcsvfiles" ADD CONSTRAINT "data_rawcsvfiles_category_id_cbf2c700_fk_data_category_id" FOREIGN KEY ("category_id") REFERENCES "data_category" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "data_rawcsvfiles_category_id_cbf2c700" ON "data_rawcsvfiles" ("category_id");
ALTER TABLE "data_kidney_sample_annotations" ADD CONSTRAINT "data_kidney_sample_a_category_id_d7d9df0b_fk_data_cate" FOREIGN KEY ("category_id") REFERENCES "data_category" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "data_kidney_sample_annotations_geom_id" ON "data_kidney_sample_annotations" USING GIST ("geom");
CREATE INDEX "data_kidney_sample_annotations_category_id_d7d9df0b" ON "data_kidney_sample_annotations" ("category_id");
ALTER TABLE "data_cell_types_for_spatial_decon" ADD CONSTRAINT "data_cell_types_for__category_id_425313ac_fk_data_cate" FOREIGN KEY ("category_id") REFERENCES "data_category" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "data_cell_types_for_spatial_decon_category_id_425313ac" ON "data_cell_types_for_spatial_decon" ("category_id");
COMMIT;
