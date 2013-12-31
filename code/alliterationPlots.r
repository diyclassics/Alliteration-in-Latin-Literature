library(plyr)

directory <- "/Users/pbartleby/Dropbox/Projects/Alliteration-in-Latin-Literature/results/"
filename <- "results.csv"

setwd(directory)

data <- read.csv('results.csv',header=TRUE)

total.words <- sum(data$words)

data.authors <- ddply(data,~author,summarise,meanAB=mean(ab),meanSAT=mean(sat)) 
data.authors.sort <- data.authors[order(data.authors$meanSAT,decreasing=TRUE),]

plotAuthors <- data.authors.sort$author
plotAB <- data.authors.sort$meanAB
plotSAT <- data.authors.sort$meanSAT
plotAB.mean <- round(mean(plotAB),2)
plotSAT.mean <- round(mean(plotSAT),2)

plotSAT <- plotSAT - plotAB # allows the stacked barplot to add up correctly; all alliterative bigrams are by definition part of the semi-alliterative trigram

plotMatrix <- cbind(plotAB,plotSAT)
rownames(plotMatrix) <- plotAuthors
colnames(plotMatrix) <- c('Alliterative Bigrams','Semi-Alliterative Trigrams')
plotMatrix <- t(plotMatrix)

par(mfrow=c(1, 1))
par(mar=c(9, 4, 4, 2) + 0.1)
par(cex=.75, cex.main=2.75, cex.lab=1.5)
par(mgp=c(6,1,0))
par(omi=c(1,.75,1,.75))
all <- barplot(plotMatrix,xaxt='n', main = "Alliteration Rates in Latin Authors 200 BCE - 200 CE", ylab = "Alliterative Samples (per 1000 words)", width = 50, space=1, density=40, legend = rownames(plotMatrix), ylim = c(0,250), col=heat.colors(2))
text(all,par("usr")[3]-0.025,srt=50,adj=c(1.1,1.1),labels = plotAuthors,xpd=TRUE,col="black")
title(xlab = "Authors", cex.lab = 1.5, line = 8)
abline(h=plotAB.mean,col='red',lty=3)
abline(h=plotSAT.mean,col='orange',lty=3)
box(which="outer",col="black")

# Seneca plots
data.seneca <- data[data$author=='Seneca the Younger',]
data.seneca.prose <- data.seneca[data.seneca$type =='P',]
data.seneca.verse <- data.seneca[data.seneca$type =='V',]
data.seneca.prose <- data.seneca.prose[order(data.seneca.prose$sat,decreasing=TRUE),]
data.seneca.verse <- data.seneca.verse[order(data.seneca.verse$sat,decreasing=TRUE),]

senP.labs <- data.seneca.prose$file
senV.labs <- data.seneca.verse$file

par(mfrow=c(1, 2))
par(cex=1, cex.main=1.5, cex.lab=1.5)
par(mgp=c(5,1,0))
par(omi=c(.5,.5,.5,.5))
    
senP <- barplot(data.seneca.prose$sat, main = "Senecan Prose", ylab = "Semi-Alliterative Trigrams (per 1000 words)",width=1,ylim = c(130,185),density=30, col='orange',xpd=FALSE)
text(senP,par("usr")[3]-0.025,srt=50,adj=c(1.1,1.1),labels = senP.labs,xpd=TRUE)
senV <- barplot(data.seneca.verse$sat, main = "Senecan Verse",width=1, ylim = c(130,185), density=30,col="yellow",xpd=FALSE)
text(senV,par("usr")[3]-0.025,srt=50,adj=c(1.1,1.1),labels = senV.labs,xpd=TRUE)

par(cex.main=2.5)
title('Comparison of Alliteration Rates in Senecan Prose and Verse',outer=TRUE)

# Genre plots
data.genre <- data[data$genre != 'Misc',]

data.genres <- ddply(data.genre,~genre,summarise,meanAB=mean(ab),meanSAT=mean(sat)) 
data.genres.sort <- data.genres[order(data.genres$meanSAT,decreasing=TRUE),]

plotGenres <- data.genres.sort$genre
plotAB.genre <- data.genres.sort$meanAB
plotSAT.genre <- data.genres.sort$meanSAT
plotAB.genre.mean <- round(mean(plotAB.genre),2)
plotSAT.genre.mean <- round(mean(plotSAT.genre),2)

plotSAT.genre <- plotSAT.genre - plotAB.genre # allows the stacked barplot to add up correctly; all alliterative bigrams are by definition part of the semi-alliterative trigram

plotMatrix.genre <- cbind(plotAB.genre,plotSAT.genre)
rownames(plotMatrix.genre) <- plotGenres
colnames(plotMatrix.genre) <- c('Alliterative Bigrams','Semi-Alliterative Trigrams')
plotMatrix.genre <- t(plotMatrix.genre)

par(mfrow=c(1, 1))
par(cex=1, cex.main=2, cex.lab=1.5)
par(mgp=c(5,1,0))
par(omi=c(.5,.5,.5,.5))
all.genre <- barplot(plotMatrix.genre,xaxt='n', main = "Alliteration Rates by genre", ylab = "Alliterative Samples (per 1000 words)", width = 50, space=1, density=50, legend = rownames(plotMatrix), ylim = c(0,250), col=heat.colors(2))
text(all.genre,par("usr")[3]-0.025,srt=50,adj=c(1.1,1.1),labels = plotGenres,xpd=TRUE)
title(xlab = "Selected Genres", cex.lab = 1.5, line = 5)

# Date plots

data.date <- ddply(data,~date,summarise,meanAB=mean(ab),meanSAT=mean(sat)) 

plotDates <- data.date$date

plotAB.date <- data.date$meanAB
plotSAT.date <- data.date$meanSAT

dates <- as.Date(data.date$date,origin="1970/1/1")

par(mfrow=c(1, 1))
par(mar=c(9, 6, 4, 2) + 0.1)
par(cex=1, cex.main=2, cex.lab=1)
par(mgp=c(4,1,0))
par(omi=c(1,.75,1,.75))

plot(data.date$meanSAT~dates,col="black",pch=16,ylab="Semi-Alliterative Trigrams (per 1000 words)",xlab="Years",main="Alliteration Rates in Latin Authors 200 BCE - 200 CE",axes=FALSE)
box(which="plot",col="black")

yrs50 <- seq(as.Date(-792576,origin="1970-01-01"),as.Date(-646479,origin="1970-01-01"),by="50 years")

axis(2)
axis(1,at=yrs50,labels=c(paste(seq(200,50,by=-50)," BCE",sep=""),"0",paste(seq(50,200,by=50)," CE",sep="")))