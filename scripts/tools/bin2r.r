
args<-vector()
args <-commandArgs(trailingOnly = TRUE)

name<-args[1]
data_save<-args[2]




#infile <-file.path(data_save, paste('data',name,'.bin', sep=''))
infile <-file.path(data_save,name)
con <- file(infile, "rb")
dim <- readBin(con, "integer", 2)
Mat <- matrix( readBin(con, "numeric", prod(dim)), dim[1], dim[2])
close(con)

name<-strsplit(name,'.bin')[[1]][1]

saveRDS(Mat, file=file.path(data_save, paste(name, '.rds', sep='') )  )