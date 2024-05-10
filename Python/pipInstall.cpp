#include "HoudiniApi.h"
#include "HoudiniEngineRuntime.h"
#include "HoudiniAssetComponent.h"

void UMyClass::PrintPythonFilesFromHDA(UHoudiniAssetComponent* HoudiniAssetComponent)
{
    if (!HoudiniAssetComponent)
        return;

    FHoudiniAssetInfo AssetInfo;
    if (HAPI_RESULT_SUCCESS != FHoudiniApi::GetAssetInfo(
        FHoudiniEngine::Get().GetSession(),
        HoudiniAssetComponent->GetAssetId(),
        &AssetInfo))
    {
        return;
    }

    // Retrieve the number of extra files
    int32 FileCount = 0;
    FHoudiniApi::GetExtraFileCount(
        FHoudiniEngine::Get().GetSession(), 
        AssetInfo.nodeId, 
        &FileCount);

    for (int32 FileIndex = 0; FileIndex < FileCount; ++FileIndex)
    {
        FString FileName;
        FHoudiniEngineString HoudiniEngineString;
        FHoudiniApi::GetExtraFileName(
            FHoudiniEngine::Get().GetSession(),
            AssetInfo.nodeId,
            FileIndex,
            HoudiniEngineString.Handle);

        HoudiniEngineString.ToFString(FileName);

        if (FileName.EndsWith(".py"))
        {
            // Read the content of the Python file
            TArray<char> FileContent;
            FHoudiniApi::GetExtraFileContent(
                FHoudiniEngine::Get().GetSession(),
                AssetInfo.nodeId,
                FileIndex,
                FileContent.GetData(),
                FileContent.Num());

            FString FileContentString(FileContent.GetData());

            // Log the file name and its content
            UE_LOG(LogTemp, Log, TEXT("Python file: %s"), *FileName);
            UE_LOG(LogTemp, Log, TEXT("Content: %s"), *FileContentString);
        }
    }
}
