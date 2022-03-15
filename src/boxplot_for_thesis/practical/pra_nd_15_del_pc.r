## read file data

d1 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=false_mcs=default_spp=default/RadarDetection_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d2 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=false_mcs=default_spp=default/Range_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d3 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=false_mcs=default_spp=default/NavSatFix_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d4 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=false_mcs=default_spp=default/RadarTrack_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")

d1 <- d1[10:1990, ]
d2 <- d2[10:1990, ]
d3 <- d3[10:1990, ]
d4 <- d4[10:1990, ]



data1 <- cbind(d1,d2,d3,d4)

d1 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=true_mcs=default_spp=default/RadarDetection_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d2 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=true_mcs=default_spp=default/Range_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d3 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=true_mcs=default_spp=default/NavSatFix_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d4 <- read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_pra_j/nd=true_mcs=default_spp=default/RadarTrack_rate=15/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")

d1 <- d1[10:1990, ]
d2 <- d2[10:1990, ]
d3 <- d3[10:1990, ]
d4 <- d4[10:1990, ]


data2 <- cbind(d1,d2,d3,d4)


all_data <- list(data1,data2)

## define x-axis scale name
xaxis_scale <- c('RadarDetection','Range','NavSatFix','RadarTrack')
# box_cols <- c("#f7f7f7", "#cccccc","#969696","#525252")                # box colors
box_cols <- c("#f7f7f7","#969696")
## border_cols <- c("red", "blue")                   # box-line colrs
border_cols <- c("black","black")                   # box-line colors
## graphic function
comparison_BoxPlot <- function(all_data) {
    ## set parameters for graph
    par(
        xaxs="i",                      # x-axis data span has no margin
        mar = c(4,6,3,2)                #  margin
    )
    ## prepare graph feild
    plot(
        0, 0, type = "n",
        xlab = expression(paste("Message Type")), ylab = expression(paste("Jitter [ms]")), # labels
        cex.lab = 2.2,                     # label font size
        font.lab = 15,                      # label font
        xlim = range(2:(ncol(data1) * 2+2)), # define large x-axis
        ylim = c(-0.04, 0.04), # y-axis data span
        font.axis = 15,                                # axis font
        cex.axis = 1.8,                       # y-axis font size
        xaxt = "n"                                    # no x-axis
    )
    ## draw vertical line
    abline(
        v = c(4, 6, 8), # position
        lwd = 1                       # line width
    )
    ## draw boxplot
    for (i in 1:2){
        boxplot(
            all_data[[i]],
            at = c(1:ncol(data1)) * 2 + i - 0.5, # position of drawing boxplot
            border   = border_cols[i],
            col = box_cols[i],                       # colors
            xaxt = "n",                          # no x-axis scale
            yaxt = "n",
            range = 1,                           # no plot outliers
            outline = FALSE,
            boxwex = 0.7,
            add = TRUE)
    }
    ## legend
    legend(
        "topleft",                      # position
        legend = c("false ","true"),   # labels
        cex = 2.3,                      # labels font size
        pt.cex = 3,                     # marker size
        pch = 22,                       # kinds of marker
        col = border_cols,              # box-line colors
        pt.bg = box_cols,               # box colors
        lty = 0,
        lwd = 1,                        # box-line width
        bg = "white"                    # background color
    )
    ## x-axis scale
    axis(
        1,
        at = 1:length(xaxis_scale) * 2+1 , # position of scale
        labels = xaxis_scale,                 # set scale name
        cex.axis=1.7,                        # axis font size
        font.axis = 15,
        tick = TRUE
    )
}
# X11(width=200, height=50)
# comparison_BoxPlot(all_data)
# output file as pdf
pdf("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/boxplot_for_thesis/practical/pra_nd_15_del_pc.pdf",width = 25, height =9)            # start rendering graph as "BoxPlot.pdf"
comparison_BoxPlot(all_data)
dev.off()            

