#include "ClassroomGameMode.h"
#include "RCCarPawn.h"
#include "RCCarInClass.h"

AClassroomGameMode::AClassroomGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
	DefaultPawnClass = ARCCarPawn::StaticClass();
}

void AClassroomGameMode::BeginPlay()
{
	super::BeginPlay();
	RemainingTime = MatchDuration;
	TotalScore = 0;
	CoinsCollected = 0;
	CurrentCombo = 0;
	bIsGameOver = false;
}

void AClassroomGameMode::Tick(float DeltaTime)
{
	super::Tick(DeltaTime);

	if (bIsGameOver) return;

	// Decrement match countdown
	RemainingTime -= DeltaTime;
	if (RemainingTime <= 0.0f)
	{
		RemainingTime = 0.0f;
		CheckTimeOut();
	}

	// Combo decay
	if (CurrentCombo > 0)
	{
		ComboTimer -= DeltaTime;
		if (ComboTimer <= 0.0f)
		{
			CurrentCombo = 0;
		}
	}
}

void AClassroomGameMode::AddScore(int32 BasePoints, int32 Coins)
{
	if (bIsGameOver) return;

	CurrentCombo++;
	ComboTimer = 3.5f;

	float Multiplier = 1.0f + (CurrentCombo - 1) * 0.25f;
	int32 Points = FMath::RoundToInt(BasePoints * Multiplier);

	TotalScore += Points;
	CoinsCollected += Coins;

	OnScoreUpdated.Broadcast(TotalScore, CoinsCollected, CurrentCombo);
}

void AClassroomGameMode::CheckTimeOut()
{
	TriggerGameOver(true, TEXT("Class Bell Rang! You successfully evaded Sensei!"));
}

void AClassroomGameMode::TriggerGameOver(bool bVictory, const FString& Reason)
{
	if (bIsGameOver) return;

	bIsGameOver = true;
	UE_LOG(LogRCCar, Log, TEXT("Game Over! Victory: %s, Reason: %s"), bVictory ? TEXT("True") : TEXT("False"), *Reason);
	OnGameOver.Broadcast(bVictory, Reason);
}
