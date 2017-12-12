library(readr)

#####  occupancy/L  #####

#occupancy of factors on all transcripts per base (length normalize)
occupancy_l <- read_delim("~/Coding/cluster/plots/Occupancy_vs_features/occupancy_divLength.txt",
                        "\t", escape_double = FALSE, trim_ws = TRUE)


######################## all in one ####################################

pvalues <- matrix(ncol=length(factors$factors), nrow=5)

i=1
for(fac in factors$factors){
  model = lm(as.formula(paste(fac, 'length + optimality + coverage + halflife', sep = '~')), data = occupancy_l)
  pvalues[,i] = -log10(ifelse(summary(model)$coefficients[,4]==0,1, summary(model)$coefficients[,4])) 
  i = i+1
}

colnames(pvalues) = factors$factors
rownames(pvalues) = c('intersect', 'length', 'optimality', 'expression', 'half-life')

write.table(pvalues, file = "~/Coding/cluster/plots/Occupancy_vs_features/pvalues_filteredvalues.txt", sep = '\t', quote = FALSE)

xx <- barplot(-log10(pvalues[(2:5),]), names.arg = c('length', 'optimality', 'expression', 'half-life'), beside=TRUE,
              cex.axis=0.6, cex.names=0.9,las=2, col = colors)
