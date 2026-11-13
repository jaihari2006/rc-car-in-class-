#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "TeacherAIController.generated.h"

class UAISenseConfig_Sight;
class UAIPerceptionComponent;
class ARCCarPawn;

UENUM(BlueprintType)
enum class ETeacherState : uint8
{
	Patrol UMETA(DisplayName = "Patrol Classroom"),
	Alert UMETA(DisplayName = "Alert / Suspicious"),
	Chase UMETA(DisplayName = "Chase RC Car"),
	Stunned UMETA(DisplayName = "Stunned"),
	Catching UMETA(DisplayName = "Catch Player")
};

UCLASS()
class RCCARINCLASS_API ATeacherAIController : public AAIController
{
	GENERATED_BODY()

public:
	ATeacherAIController();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Sensei | State")
	ETeacherState CurrentState = ETeacherState::Patrol;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float SightRadius = 1400.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float LoseSightRadius = 1800.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float PeripheralVisionAngle = 65.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float CatchDistance = 180.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float WalkSpeed = 320.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sensei | AI")
	float ChaseSpeed = 650.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Sensei | AI")
	ARCCarPawn* TargetCar = nullptr;

	UFUNCTION()
	void OnPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus);

	UFUNCTION(BlueprintCallable, Category = "Sensei | Action")
	void StunTeacher(float Duration);

private:
	void UpdatePatrol();
	void UpdateChase(float DeltaTime);
	void CheckCatch();

	FTimerHandle StunTimerHandle;
	void RecoverFromStun();

	TArray<FVector> ClassroomWaypoints;
	int32 CurrentWaypointIndex = 0;
	float PatrolWaitTimer = 0.0f;
};
