source("packages.R")
source("config.R")

ui <- dashboardPage(
  skin = "black",
  
  # le DASHBOARD HEADER
  dashboardHeader(title = "Dashboard"),
  
  
  # le DASHBOARD SIDEBAR
  dashboardSidebar(
    
    
    
    
    # les options sidebar
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
    ),
    
    
    
    
    sidebarMenu(
      menuItem("COMPARAISON", tabName = "ONGLET_draft", icon = icon("plane")),
      menuItem("DATAFRAME", tabName = "ONGLET_offset", icon = icon("plane")),
      # menuItem("HABITS", tabName = "ONGLET_habits", icon = icon("plane")),
      # menuItem("RECHERCHE", tabName = "ONGLET_recherche", icon = icon("plane")),
    
      selectInput(
        inputId = "selected_id",
        label = "Selectionnez une paire", 
        choices = df$id,
        selected = 1,
        selectize = TRUE
      ),

      
      
      # actionButton(inputId = "button_next",label ="Suivant"),
      
      radioButtons(inputId="decision",
                   label="Faites votre choix",
                   choices = c("match","doubt","unmatch","cont diff"),
                   selected = NULL,
                   inline = FALSE,
                   width = NULL,
                   choiceNames = NULL,
                   choiceValues = NULL),
      actionButton("goButton", "Save")
      
      
      
      
    ) # fin de la sidebar menu
    
    
    
    
  ), # fin de la dashboardsidebar
  
  
  
  
  
  # LE DASHBOARD BODY
  dashboardBody(
    
    # Les styles
    tags$style(type="text/css",
               ".shiny-output-error { visibility: hidden; }",
               ".shiny-output-error:before { visibility: hidden; }"
    ),

    
    
    
    
    
    
    tabItems(
      
      
      
      
      
      
      
      # Debut onglet draft
      tabItem(
        tabName = "ONGLET_draft",
        
        
        # ROW 1 - Onglet draft
        # Nouvelle Fluidrow pour afficher
        fluidRow(
            valueBoxOutput("score",width=6),
            valueBoxOutput("truth",width=6)
        ),
        
        
        fluidRow(
          box(
            collapsible = TRUE,
            collapsed = FALSE,
            solidHeader = TRUE,
            status = "primary",
            title="URL A",
            width=6,
            htmlOutput("frame1")
          ),
          box(
            collapsible = TRUE,
            collapsed = FALSE,
            solidHeader = TRUE,
            status = "primary",
            title="URL B",
            width=6,
            htmlOutput("frame2")
          )
        ),
        fluidRow(
          box(
            collapsible = TRUE,
            collapsed = FALSE,
            solidHeader = TRUE,
            status = "primary",
            title="Carte des geoclusters de l'id",
            width=6,
            verbatimTextOutput("info")
          )
        ),
        fluidRow(
        ),
        fluidRow(
        ),
        fluidRow(
        ),
        fluidRow(
        )
   
      ), # FIN ONGLET draft
      
      
      
      
      
      
      # Debut onglet offset
      tabItem(
        tabName = "ONGLET_offset",
        
        # ROW 1 - Onglet offset
        fluidRow(
          box(
            collapsible = TRUE,
            collapsed = FALSE,
            solidHeader = TRUE,
            status = "primary",
            title="Dataframe des paires",
            width=12,
            tableOutput("matable")
          )

        )
      ) # FIN ONGLET OFFSET, rajouter virgule apres parenthese si autre onglet
      
      
      
      
      
      # # début Onglet habits
      # tabItem(
      #   tabName = "ONGLET_habits",
      #   
      #   # ROW 1 - Onglet HABITS
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   ),
      #   fluidRow(
      #   )
      # ), # fin onglet habits
      
      
      
      
      
      # Debut onglet RECHERCHE
      # tabItem(
      #   tabName = "ONGLET_recherche",
      #   # R1 - Onglet recherche
      #   fluidRow(
      #   )
      # ) # Fin ONGLET RECHERCHE
      
      
      
      
      
      
      
      
      
    ) # fin de tabitems global
    
    
    
    
    
    
    ) # fin dashboard body
  
  
  ) # fin dashboard page















