#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "ClassroomGameMode.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnGameOverSignature, bool, bVictory, const FString&, Reason);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnScoreUpdatedSignature, int32, NewScore, int32, NewCoins, int32, CurrentCombo);

UCLASS()
class RCCARINCLASS_API AClassroomGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AClassroomGameMode();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Rules")
	float MatchDuration = 120.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game Rules")
	float RemainingTime = 120.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game Stats")
	int32 TotalScore = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game Stats")
	int32 CoinsCollected = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game Stats")
	int32 CurrentCombo = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game Stats")
	float ComboTimer = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Rules | Multiplayer")
	bool bIsSenseiTagMode = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game State")
	bool bIsGameOver = false;

	UFUNCTION(BlueprintCallable, Category = "Game Rules")
	void AddScore(int32 BasePoints, int32 Coins);

	UFUNCTION(BlueprintCallable, Category = "Game Rules")
	void TriggerGameOver(bool bVictory, const FString& Reason);

	UPROPERTY(BlueprintAssignable, Category = "Events")
	FOnGameOverSignature OnGameOver;

	UPROPERTY(BlueprintAssignable, Category = "Events")
	FOnScoreUpdatedSignature OnScoreUpdated;

private:
	void CheckTimeOut();
};
