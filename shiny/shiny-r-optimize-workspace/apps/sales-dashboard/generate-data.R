# Deterministic data generator for the sales-dashboard fixture.
# Run from this directory: Rscript generate-data.R  (writes sales.csv here)
set.seed(42)

regions <- c("North", "South", "East", "West")
base_cities <- c(North = "Springfield", South = "Riverton",
                 East = "Laketown", West = "Hillcrest")
products <- c("Widget", "Gadget", "Doohickey", "Contraption", "Gizmo", "Thingamajig")
categories <- c("Hardware", "Software", "Services")
dates <- seq(as.Date("2019-01-01"), as.Date("2023-12-31"), by = "day")

n_per_region <- 50000  # 4 regions x 50k = 200k rows

make_region <- function(region, n) {
  data.frame(
    date = sample(dates, n, replace = TRUE),
    region = region,
    city = paste0(unname(base_cities[region]), " ", sample(1:3, n, replace = TRUE)),
    product = sample(products, n, replace = TRUE),
    category = sample(categories, n, replace = TRUE, prob = c(.5, .3, .2)),
    units = sample(1:20, n, replace = TRUE),
    stringsAsFactors = FALSE
  )
}

sales <- do.call(rbind, lapply(regions, make_region, n = n_per_region))

# Revenue with mild seasonality + noise; deterministic given the seed
doy <- as.numeric(strftime(sales$date, format = "%j"))
sales$revenue <- round(
  sales$units * (50 + 10 * sin(2 * pi * doy / 365) + rnorm(nrow(sales), 0, 5)),
  2
)

sales <- sales[order(sales$date), ]
write.csv(sales, "sales.csv", row.names = FALSE)
cat("wrote sales.csv with", nrow(sales), "rows\n")
