library(dplyr, warn.conflicts = FALSE)
library(tidyr)

extrair_data <- function(data, tipo.dado) {
  data.str <- toString(data)
  if(nchar(data.str) == 5 ){
    data.str = paste(0, data.str, sep="")
  }
  if(tipo.dado == "m") {
    return(substr(data.str , 1, 2))
  } else if(tipo.dado == "a"){
    return(substr(data.str , 2, 6))
  }
  return(data.str)

}


folha_pessoal <-  read.csv("~/ufcg/hackfest/zip sagres/TCE-PB-SAGRES-Folha_Pessoal_Esfera_Municipal_camaras.txt", 
                           header=FALSE, sep=";", encoding = "UTF-8")

folha_pessoal_copia <- folha_pessoal


#caso não tenha o nome das colunas
colnames(folha_pessoal_copia) <- c("cd_UGestora", "de_ugestora", "de_cargo", "de_tipocargo", "cd_CPF", 
                 "dt_MesAnoReferencia", "no_Servidor", "de_UOrcamentaria")

folha_pessoal_copia <- folha_pessoal_copia %>%
  separate(de_ugestora, c("orgao", "cidade"), " de ")

folha_pessoal_copia <- folha_pessoal_copia %>%
  rowwise() %>%
  mutate(mes= extrair_data(dt_MesAnoReferencia, "m"), ano= extrair_data(dt_MesAnoReferencia, "a"))




cargos <- folha_pessoal_copia %>%
  group_by(de_cargo) %>%
  summarise(quantidade = length(de_cargo))%>%
  arrange(quantidade)


tipo_cargo <-folha_pessoal_copia %>%
  group_by(de_tipocargo) %>%
  summarise(quantidade = length(de_tipocargo)) %>%
  arrange(quantidade)


write.csv(cargos, file = "~/ufcg/hackfest/cargos.csv", fileEncoding="UTF-8", row.names=FALSE)
write.csv(tipo_cargo, file = "~/ufcg/hackfest/tipo_cargos.csv", fileEncoding="UTF-8", row.names=FALSE)

folha_pessoal_copia <- folha_pessoal_copia %>%
  separate(de_ugestora, c("orgao", "cidade"), " de ")

cargos_cidade <- folha_pessoal_copia %>%
  group_by(cidade, de_cargo) %>%
  summarise(quantidade = length(de_cargo))%>%
  arrange(cidade)


tipo_cargo_cidade <-folha_pessoal_copia %>%
  group_by(cidade, de_tipocargo) %>%
  summarise(quantidade = length(de_tipocargo)) %>%
  arrange(cidade)

write.csv(cargos_cidade, file = "~/ufcg/hackfest/cargos_cidade.csv", fileEncoding="UTF-8", row.names=FALSE)
write.csv(tipo_cargo_cidade, file = "~/ufcg/hackfest/tipo_cargos_cidade.csv", fileEncoding="UTF-8", row.names=FALSE)


arquivo_final <- folha_pessoal_copia %>%
  select(cd_UGestora, cidade, orgao, de_cargo, de_tipocargo, cd_CPF, no_Servidor,  mes, ano)

write.csv(arquivo_final, file = "~/ufcg/hackfest/arquivo_completo_camara.csv", fileEncoding="UTF-8", row.names=FALSE)


