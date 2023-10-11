#pragma once
#include "Engine.hpp"
#include <iostream>

namespace Engine {
	struct BlueprintFunctionInfo {
		std::wstring parent_name;
		std::wstring function_name;
		void* params;
	};

	std::vector<BlueprintFunctionInfo> blueprint_function_queue;
	std::vector<std::function<void (UObject*)>> function_queue;

	UWorld* Engine::GetWorld() {
		UObject* player_controller = UObjectGlobals::FindFirstOf(STR("PlayerController"));
		return static_cast<AActor*>(player_controller)->GetWorld();
	}

	void Engine::ExecuteInGameThread(std::function<void(UObject*)> function) {
		function_queue.push_back(function);
	}

	void Engine::ExecuteBlueprintFunction(std::wstring new_parent, std::wstring new_name, void* params) {
		blueprint_function_queue.push_back(BlueprintFunctionInfo(new_parent, new_name, params));
	}

	void Engine::OnTick(UObject* blueprint) {
		for (BlueprintFunctionInfo& info : blueprint_function_queue) {
			UObject* parent = UObjectGlobals::FindFirstOf(info.parent_name);
			if (!parent) {
				// TODO: return an error
				return;
			}
			UFunction* function = parent->GetFunctionByName(info.function_name.c_str());
			if (!function) {
				// TODO: return an error
				return;
			}
			parent->ProcessEvent(function, info.params);
			delete info.params;
		}
		blueprint_function_queue.clear();

		for (auto& function : function_queue) {
			function(blueprint);
		}
		function_queue.clear();
	}

	void Engine::SpawnCollectibles() {
		struct CollectibleSpawnInfo {
			int64_t id;
			FVector position;
		};
		std::vector<GameData::Collectible> collectible_vector = GameData::GetCollectiblesOfZone(GetWorld()->GetName());
		for (GameData::Collectible collectible : collectible_vector) {
			if (!collectible.IsChecked()) {
				void* collectible_info = new CollectibleSpawnInfo{ collectible.GetID(), collectible.GetPosition() };
				ExecuteBlueprintFunction(L"BP_APRandomizerInstance_C", L"AP_SpawnCollectible", collectible_info);
			}
		}
	}

	void Engine::SyncItems() {
		// Call blueprint functions to sync health pieces, small keys, major keys, and upgrades
		void* hp_params = new int(GameData::GetHealthPieces());
		ExecuteBlueprintFunction(L"BP_APRandomizerInstance_C", L"AP_SetHealthPieces", hp_params);

		void* small_key_params = new int(GameData::GetSmallKeys());
		ExecuteBlueprintFunction(L"BP_APRandomizerInstance_C", L"AP_SetSmallKeys", small_key_params);

		// TODO: reconfigure major keys to be an int and reconfigure this function
		struct MajorKeyInfo {
			int index;
			bool to_give;
		};
		bool* major_keys = GameData::GetMajorKeys();
		for (int i = 0; i < 5; i++)
		{
			void* major_key_params = new MajorKeyInfo{ i, major_keys[i] };
			ExecuteBlueprintFunction(L"BP_APRandomizerInstance_C", L"AP_SetMajorKey", major_key_params);
		}

		struct AddUpgradeInfo {
			FName name;
			int count;
		};
		for (auto const& pair : GameData::GetUpgradeTable()) {
			std::unique_ptr<FName> new_name(new FName(pair.first));
			void* upgrade_params = new AddUpgradeInfo{ *new_name, pair.second };
			ExecuteBlueprintFunction(L"BP_APRandomizerInstance_C", L"AP_AddUpgrade", upgrade_params);
		}
	}
}