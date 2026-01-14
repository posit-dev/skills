# shiny-react utility functions for R
# Copy this file to your project's r/ directory
#
# Provides:
#   page_react() - Creates HTML page with React mounting point
#   render_json() - Renders arbitrary JSON data to React
#   post_message() - Sends custom messages to React components
#
# License: MIT 2025, Posit Software, PBC
# Source: https://github.com/wch/create-shiny-react-app/blob/main/templates/2-scaffold/r/shinyreact.R

library(shiny)

page_bare <- function(..., title = NULL, lang = NULL) {
  ui <- list(
    shiny:::jqueryDependency(),
    if (!is.null(title)) tags$head(tags$title(title)),
    ...
  )
  attr(ui, "lang") <- lang
  ui
}

page_react <- function(
  ...,
  title = NULL,
  js_file = "main.js",
  css_file = "main.css",
  lang = "en"
) {
  page_bare(
    title = title,
    tags$head(
      if (!is.null(js_file)) tags$script(src = js_file, type = "module"),
      if (!is.null(css_file)) tags$link(href = css_file, rel = "stylesheet")
    ),
    tags$div(id = "root"),
    ...
  )
}


#' Reactively render arbitrary JSON object data.
#'
#' This is a generic renderer that can be used to render any Jsonifiable data.
#' The data goes through shiny:::toJSON() before being sent to the client.
render_json <- function(
  expr,
  env = parent.frame(),
  quoted = FALSE,
  outputArgs = list(),
  sep = " "
) {
  func <- installExprFunction(
    expr,
    "func",
    env,
    quoted,
    label = "render_json"
  )

  createRenderFunction(
    func,
    function(value, session, name, ...) {
      value
    },
    function(...) {
      stop("Not implemented")
    },
    outputArgs
  )
}

#' Send a custom message to the client
#'
#' A convenience function for sending custom messages from the Shiny server to
#' React components using useShinyMessageHandler() hook. This wraps messages in a
#' standard format and sends them via the "shinyReactMessage" channel.
#'
#' When used within a Shiny module (moduleServer), the type is automatically
#' namespaced using session$ns(). Outside of modules, the type is passed through
#' unchanged.
#'
#' @param session The Shiny session object
#' @param type The message type (should match messageType in useShinyMessageHandler)
#' @param data The data to send to the client
post_message <- function(session, type, data) {
  namespaced_type <- session$ns(type)
  session$sendCustomMessage(
    "shinyReactMessage",
    list(
      type = namespaced_type,
      data = data
    )
  )
}
