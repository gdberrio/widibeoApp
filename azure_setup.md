# Storage Acccount

widibeoappdatalake

# Resource Group

widibeoApp

az ad signed-in-user show --query id -o tsv | az role assignment create \
 --role "Storage Blob Data Contributor" \
 --assignee @- \
 --scope "/subscriptions/6db5c977-2d8c-4c91-afc6-713ffd5920ce/resourceGroups/widibeoApp/providers/Microsoft.Storage/storageAccounts/widibeoappdatalake"

az storage container create \
 --account-name widibeoappdatalake \
 --name widibeotestcontainer \
 --auth-mode login

az storage blob upload \
 --account-name widibeoappdatalake \
 --container-name widibeotestcontainer \
 --name upload_test.txt \
 --file upload_test.txt \
 --auth-mode login
