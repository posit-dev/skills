# Model Explorer — fit a response model to survey data
library(shiny)
library(bslib)
library(ggplot2)

ui <- page_fixed(
  title = "Model Explorer",
  h2("Customer survey response model"),
  p("Fit a response-time model to the survey dataset, then explore the results."),
  input_task_button("fit", "Fit model"),
  p(textOutput("clock", inline = TRUE), style = "color: silver;"),
  hr(),
  layout_column_wrap(
    width = 1 / 2,
    card(card_header("Observed vs. predicted"), plotOutput("pred_plot")),
    card(card_header("Residual diagnostics"), plotOutput("resid_plot")),
    card(card_header("Coefficients"), verbatimTextOutput("coefs")),
    card(card_header("Fit summary"), verbatimTextOutput("summary"))
  )
)

server <- function(input, output, session) {
  survey <- read.csv("survey.csv", stringsAsFactors = FALSE)

  fit <- eventReactive(input$fit, {
    Sys.sleep(4)
    lm(response_time ~ age + channel + prior_purchases + satisfaction,
       data = survey)
  })

  output$pred_plot <- renderPlot({
    m <- fit()
    survey$pred <- predict(m, newdata = survey)
    ggplot(survey, aes(pred, response_time)) +
      geom_point(alpha = 0.3) +
      geom_abline(slope = 1, intercept = 0, color = "red") +
      labs(title = "Observed vs. predicted response time", x = "Predicted", y = "Observed")
  })

  output$resid_plot <- renderPlot({
    m <- fit()
    ggplot(data.frame(resid = residuals(m), fitted = fitted(m)),
           aes(fitted, resid)) +
      geom_point(alpha = 0.3) +
      geom_hline(yintercept = 0, color = "red") +
      labs(title = "Residuals vs. fitted", x = "Fitted", y = "Residual")
  })

  output$coefs <- renderPrint({
    m <- fit()
    round(coef(m), 4)
  })

  output$summary <- renderPrint({
    m <- fit()
    s <- summary(m)
    cat(sprintf("R-squared: %.3f\nResidual SE: %.2f\nObservations: %d\n",
                s$r.squared, s$sigma, s$df[2] + s$df[1]))
  })

  # Live clock
  output$clock <- renderText({
    invalidateLater(1000)
    format(Sys.time(), "%H:%M:%S")
  })
}

shinyApp(ui, server)
