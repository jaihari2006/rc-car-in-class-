#include "TeacherAIController.h"
#include "Perception/AIPerceptionComponent.h"
#include "Perception/AISenseConfig_Sight.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "RCCarPawn.h"
#include "ClassroomGameMode.h"
#include "RCCarInClass.h"

ATeacherAIController::ATeacherAIController()
{
	PrimaryActorTick.bCanEverTick = true;

	UAIPerceptionComponent* PerceptionComp = CreateDefaultSubobject<UAIPerceptionComponent>(TEXT("PerceptionComponent"));
	SetPerceptionComponent(*PerceptionComp);

	UAISenseConfig_Sight* SightConfig = CreateDefaultSubobject<UAISenseConfig_Sight>(TEXT("SightConfig"));
	SightConfig->SightRadius = SightRadius;
	SightConfig->LoseSightRadius = LoseSightRadius;
	SightConfig->PeripheralVisionAngleDegrees = PeripheralVisionAngle;
	SightConfig->DetectionByAffiliation.bDetectEnemies = true;
	SightConfig->DetectionByAffiliation.bDetectNeutrals = true;
	SightConfig->DetectionByAffiliation.bDetectFriendlies = true;

	PerceptionComp->ConfigureSense(*SightConfig);
	PerceptionComp->SetDominantSense(SightConfig->GetSenseClass());
}

void ATeacherAIController::BeginPlay()
{
	super::BeginPlay();

	if (GetPerceptionComponent())
	{
		GetPerceptionComponent()->OnTargetPerceptionUpdated.AddDynamic(this, &ATeacherAIController::OnPerceptionUpdated);
	}

	// Classroom navigation waypoints across desk aisles
	ClassroomWaypoints.Add(FVector(-500.0f, -400.0f, 0.0f));
	ClassroomWaypoints.Add(FVector(500.0f, -400.0f, 0.0f));
	ClassroomWaypoints.Add(FVector(500.0f, 0.0f, 0.0f));
	ClassroomWaypoints.Add(FVector(-500.0f, 0.0f, 0.0f));
	ClassroomWaypoints.Add(FVector(-500.0f, 400.0f, 0.0f));
	ClassroomWaypoints.Add(FVector(500.0f, 400.0f, 0.0f));

	TargetCar = Cast<ARCCarPawn>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
}

void ATeacherAIController::Tick(float DeltaTime)
{
	super::Tick(DeltaTime);

	if (CurrentState == ETeacherState::Stunned) return;

	if (CurrentState == ETeacherState::Chase && TargetCar)
	{
		UpdateChase(DeltaTime);
		CheckCatch();
	}
	else if (CurrentState == ETeacherState::Patrol)
	{
		UpdatePatrol();
	}
}

void ATeacherAIController::OnPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus)
{
	ARCCarPawn* DetectedCar = Cast<ARCCarPawn>(Actor);
	if (DetectedCar)
	{
		if (Stimulus.WasSuccessfullySensed())
		{
			TargetCar = DetectedCar;
			CurrentState = ETeacherState::Chase;

			ACharacter* TeacherChar = Cast<ACharacter>(GetPawn());
			if (TeacherChar && TeacherChar->GetCharacterMovement())
			{
				TeacherChar->GetCharacterMovement()->MaxWalkSpeed = ChaseSpeed;
			}
			UE_LOG(LogRCCar, Warning, TEXT("Sakamoto Sensei spotted the RC Car! Starting Chase!"));
		}
		else
		{
			// Lost sight
			CurrentState = ETeacherState::Patrol;
			ACharacter* TeacherChar = Cast<ACharacter>(GetPawn());
			if (TeacherChar && TeacherChar->GetCharacterMovement())
			{
				TeacherChar->GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
			}
		}
	}
}

void ATeacherAIController::UpdateChase(float DeltaTime)
{
	if (!TargetCar) return;
	MoveToActor(TargetCar, CatchDistance * 0.7f, true, true, false);
}

void ATeacherAIController::CheckCatch()
{
	if (!TargetCar || TargetCar->bIsCaughtBySensei) return;

	APawn* TeacherPawn = GetPawn();
	if (!TeacherPawn) return;

	float Dist = FVector::Dist(TeacherPawn->GetActorLocation(), TargetCar->GetActorLocation());
	if (Dist <= CatchDistance)
	{
		CurrentState = ETeacherState::Catching;
		TargetCar->bIsCaughtBySensei = true;

		AClassroomGameMode* GM = Cast<AClassroomGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
		if (GM)
		{
			GM->TriggerGameOver(false, TEXT("Caught by Sakamoto Sensei!"));
		}
		UE_LOG(LogRCCar, Error, TEXT("Sakamoto Sensei caught the RC car!"));
	}
}

void ATeacherAIController::UpdatePatrol()
{
	if (ClassroomWaypoints.Num() == 0) return;

	APawn* TeacherPawn = GetPawn();
	if (!TeacherPawn) return;

	FVector TargetWp = ClassroomWaypoints[CurrentWaypointIndex];
	float Dist = FVector::Dist(TeacherPawn->GetActorLocation(), TargetWp);

	if (Dist < 120.0f)
	{
		CurrentWaypointIndex = (CurrentWaypointIndex + 1) % ClassroomWaypoints.Num();
		MoveToLocation(ClassroomWaypoints[CurrentWaypointIndex], 60.0f);
	}
	else
	{
		MoveToLocation(TargetWp, 60.0f);
	}
}

void ATeacherAIController::StunTeacher(float Duration)
{
	CurrentState = ETeacherState::Stunned;
	StopMovement();

	GetWorldTimerManager().SetTimer(StunTimerHandle, this, &ATeacherAIController::RecoverFromStun, Duration, false);
	UE_LOG(LogRCCar, Log, TEXT("Sensei is stunned for %f seconds!"), Duration);
}

void ATeacherAIController::RecoverFromStun()
{
	CurrentState = ETeacherState::Patrol;
	UpdatePatrol();
}
