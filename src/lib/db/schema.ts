import { pgTable, serial, varchar, integer, text } from "drizzle-orm/pg-core";

export const tricks = pgTable("tricks", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  slug: varchar("slug", { length: 120 }).notNull().unique(),
  difficulty: integer("difficulty").notNull(),
  category: varchar("category", { length: 50 }).notNull(),
  props: varchar("props", { length: 50 }).notNull(),
  tutorial: text("tutorial"),
  video_url: varchar("video_url", { length: 300 })
});
