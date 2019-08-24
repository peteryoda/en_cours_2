shinyServer(function(input, output, session) {
  
  # R reactif
  geturls <- reactive({
    tempdf = df[df$id==input$selected_id,]
    solution = tempdf[,c("filea","fileb")]
    solution = as.vector(solution)
    solution
  })
  
  
  values <- reactiveValues(df_data = df)
  
  
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
    # geturls()
    table(values$df_data$decision)
    #3+4
  })
  
  
  
  
  
  
  
  })