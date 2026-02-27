// Define names and location
param location string = resourceGroup().location
param prefix string = 'smartapi${uniqueString(resourceGroup().id)}'

// 1. Storage Account (To save uploaded images)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${prefix}storage'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

// 2. Azure AI Vision (The "Brain")
resource aiService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${prefix}vision'
  location: location
  kind: 'ComputerVision'
  sku: { name: 'S1' }
  properties: {
    customSubDomainName: '${prefix}vision'
  }
}

// 3. Hosting Plan (Serverless - you only pay when code runs)
resource hostingPlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${prefix}plan'
  location: location
  sku: { name: 'Y1', tier: 'Dynamic' }
}

// 4. The Function App (Your Python Logic)
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: '${prefix}func'
  location: location
  kind: 'functionapp,linux'
  identity: { type: 'SystemAssigned' } // This gives the app its own "ID"
  properties: {
    serverFarmId: hostingPlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        { name: 'AzureWebJobsStorage', value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}' }
        { name: 'VISION_ENDPOINT', value: aiService.properties.endpoint }
        { name: 'VISION_KEY', value: aiService.listKeys().key1 }
      ]
    }
  }
}