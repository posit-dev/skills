# Sales Dashboard — regional revenue explorer
library(shiny)
library(bslib)
library(dplyr)
library(ggplot2)
library(DT)

ui <- page_sidebar(
  title = "Sales Dashboard",
  sidebar = sidebar(
    selectInput("region", "Region", choices = c("All", "North", "South", "East", "West")),
    sliderInput("year", "Year range", 2019, 2023, value = c(2019, 2023), step = 1),
    uiOutput("city_ui"),
    selectInput("product", "Product", choices = c("All", "Widget", "Gadget", "Doohickey", "Contraption", "Gizmo", "Thingamajig"))
  ),
  layout_column_wrap(
    width = 1 / 2,
    card(card_header("Monthly revenue"), plotOutput("revenue_plot")),
    card(card_header("Revenue summary"), verbatimTextOutput("revenue_summary")),
    card(card_header("Top products"), plotOutput("top_products")),
    card(card_header("Category mix"), plotOutput("category_mix")),
    card(card_header("Store detail (scatter)"), plotOutput("store_scatter")),
    card(card_header("Benchmark vs. competitors"), plotOutput("benchmark_plot")),
    card(card_header("Detail table"), DTOutput("detail_table"))
  )
)

server <- function(input, output, session) {
  sales <- read.csv("sales.csv", stringsAsFactors = FALSE)

  # Some prep work
  sales$month <- as.Date(format(as.Date(sales$date), "%Y-%m-01"))
  sales$year <- as.integer(format(as.Date(sales$date), "%Y"))

  # The city list depends on the region
  output$city_ui <- renderUI({
    cities <- sort(unique(sales[sales$region == input$region, "city"]))
    if (input$region == "All") cities <- sort(unique(sales$city))
    selectInput("city", "City", choices = c("All", cities))
  })

  # Helper for filtering
  filter_sales <- function(df) {
    if (input$region != "All") df <- df[df$region == input$region, ]
    df <- df[df$year >= input$year[1] & df$year <= input$year[2], ]
    if (!is.null(input$city) && input$city != "All") df <- df[df$city == input$city, ]
    if (input$product != "All") df <- df[df$product == input$product, ]
    df
  }

  output$revenue_plot <- renderPlot({
    d <- filter_sales(sales)
    agg <- aggregate(revenue ~ month, data = d, FUN = sum)
    ggplot(agg, aes(month, revenue)) +
      geom_line(color = "steelblue", linewidth = 1) +
      labs(title = "Monthly revenue", x = NULL, y = "Revenue ($)")
  })

  output$revenue_summary <- renderText({
    d <- filter_sales(sales)
    total <- sum(d$revenue)
    avg <- mean(d$revenue)
    n <- nrow(d)
    sprintf("Total revenue: $%.0f\nAverage per sale: $%.2f\nNumber of sales: %d", total, avg, n)
  })

  output$top_products <- renderPlot({
    d <- filter_sales(sales)
    agg <- aggregate(revenue ~ product, data = d, FUN = sum)
    agg <- agg[order(agg$revenue, decreasing = TRUE), ][1:6, ]
    agg$product <- factor(agg$product, levels = agg$product)
    ggplot(agg, aes(product, revenue)) +
      geom_col(fill = "darkorange") +
      coord_flip() +
      labs(title = "Top products by revenue", x = NULL, y = "Revenue ($)")
  })

  output$category_mix <- renderPlot({
    d <- filter_sales(sales)
    agg <- aggregate(revenue ~ category, data = d, FUN = sum)
    ggplot(agg, aes(x = "", y = revenue, fill = category)) +
      geom_col(width = 1) +
      coord_polar(theta = "y") +
      labs(title = "Revenue by category", x = NULL, y = NULL)
  })

  output$store_scatter <- renderPlot({
    d <- filter_sales(sales)
    ggplot(d, aes(units, revenue)) +
      geom_point(alpha = 0.4) +
      labs(title = "Units vs. revenue", x = "Units", y = "Revenue ($)")
  })

  # Compare with competitor benchmark data from our market research API
  benchmark_data <- reactive({
    Sys.sleep(1.5)
    data.frame(
      product = c("Widget", "Gadget", "Doohickey", "Contraption", "Gizmo", "Thingamajig"),
      competitor_avg = c(120000, 95000, 88000, 61000, 45000, 31000)
    )
  })

  output$benchmark_plot <- renderPlot({
    d <- filter_sales(sales)
    ours <- aggregate(revenue ~ product, data = d, FUN = sum)
    combined <- merge(ours, benchmark_data(), by = "product", all = TRUE)
    names(combined)[names(combined) == "revenue"] <- "ours"
    combined$ours[is.na(combined$ours)] <- 0
    ggplot(combined, aes(product)) +
      geom_col(aes(y = ours, fill = "Ours")) +
      geom_col(aes(y = competitor_avg, fill = "Competitor avg"), alpha = 0.5) +
      coord_flip() +
      labs(title = "Revenue vs. competitor benchmark", x = NULL, y = "Revenue ($)", fill = NULL)
  })

  output$detail_table <- renderDT({
    d <- filter_sales(sales)
    datatable(
      d[, c("date", "region", "city", "product", "category", "units", "revenue")],
      rownames = FALSE
    )
  }, server = FALSE)
}

shinyApp(ui, server)
