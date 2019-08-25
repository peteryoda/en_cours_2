shinyServer(function(input, output, session) {
  
  values <- reactiveValues(df_data = df)
  
  # Reactive values
  geturls <- reactive({
    tempdf = df[df$id==input$selected_id,]
    solution = tempdf[,c("filea","fileb")]
    solution = as.vector(solution)
    solution
  })
  
  # Reactive values
  value_box_data <- reactive({
    tempdf = df[df$id==input$selected_id,]
    solution = tempdf[,c("strate_var_score","confidence_score","decision")]
    solution = as.vector(solution)
    solution
  })
  
  
  
  # Affiche le score d'un couple en haut à gauche
  # Pour accéder à la bibliothèque des couleurs disponibles :
  # https://rstudio.github.io/shinydashboard/appearance.html
  # Pour accéder à la bibliothèque des logos
  # https://getbootstrap.com/docs/3.3/components/#glyphicons
  output$score <- renderValueBox({
    vals <- value_box_data()
    score = round(vals["confidence_score"],2)
    strate = vals$strate
    
    nmatchbystrate = statsbystrate$f[statsbystrate$strate_var_score==vals$strate_var_score]
    
    toprint1 = paste0("Model Score : ",score)
    # toprint2 = paste0("Décile n° ",strate)
    toprint2 = paste0("Décile n° ",strate, ": il y a ",nmatchbystrate," match dans ce décile")
    valueBox(
      value = toprint1,
      subtitle = toprint2,
      color = "light-blue",
      icon = icon("signal",lib="glyphicon")
    )
  })
  
  
  output$truth <- renderValueBox({
    vals <- value_box_data()
    truth = str_to_title(vals$decision)
    
    if (truth=="Match") {
      col = "green"} else {
        col = "red"
      }
    
    # nmatchbystrate = statsbystrate$f[statsbystrate$strate_var_score==vals$strate_var_score]
    
    toprint1 = paste0("Réalité : ",truth)
    # toprint2 = paste0("Il y a ",nmatchbystrate," match dans ce décile")
    valueBox(
      value = toprint1,
      subtitle = "",
      color = col,
      icon = icon("asterisk",lib="glyphicon")
    )
  })  

  
  

  
  output$frame1 <- renderUI({
    my_test <- tags$iframe(src=geturls()[["filea"]],seamless="seamless",
                           height=500,
                           width=500)
    my_test
  })
  
  
  output$frame2 <- renderUI({
    my_test <- tags$iframe(src=geturls()[["fileb"]],seamless="seamless",
                           height=500,
                           width=500)
    my_test
  })
  
  
  observeEvent(input$goButton, {
    values$df_data$decision[values$df_data$id==input$selected_id] <- input$decision
    saveRDS(object = values$df_data,"saved.rds")

  })
  
  
output$matable <-renderTable({
  values$df_data
})
    
  output$info <- renderPrint({

    value_box_data()$confidence_score

  })
  
  
  
  
  
  
  
  })