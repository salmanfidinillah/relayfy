# Hasil pengujian aktual

Synthetic core, web auth/ACL/version, model HTTP adapter fixture, scoped WorkBuddy job queue, actual HTTP CLI and MCP stdio protocol. Model replies in tests are fixtures: NOT actual LLM inference, WorkBuddy application use, or official tests

Run UTC: 2026-11-06T06:26:35.725779+00:00

84/84 lulus.

| Kasus | Hasil |
|---|---|
| test_actual_http_cli_and_mcp_tools_with_fixture_reply | PASS |
| test_brief_job_private_until_human_review | PASS |
| test_cancel_processing_invalidates_result | PASS |
| test_context_preparation_revision_cannot_be_reused | PASS |
| test_context_purpose_separates_private_ask_and_recipient_brief | PASS |
| test_demo_disabled_by_default_and_synthetic_profiles_seed_once | PASS |
| test_extractive_fallback_is_labeled_without_ai | PASS |
| test_failed_worker_no_fake_success | PASS |
| test_finish_transaction_rolls_back_when_audit_fails | PASS |
| test_forged_citation_and_quote_rejected_no_history | PASS |
| test_job_expired_lease_can_be_reclaimed | PASS |
| test_pair_is_scoped_and_key_hashed | PASS |
| test_pair_rotation_invalidates_old_key_and_lease | PASS |
| test_pending_limit_and_other_account_cancel | PASS |
| test_real_job_flow_and_revision_history | PASS |
| test_replay_and_wrong_lease_rejected | PASS |
| test_revocation_invalidates_pair_job_history_and_payload | PASS |
| test_unknown_has_no_job_and_no_restricted_existence | PASS |
| test_worker_denies_browser_and_nonloopback | PASS |
| test_worker_for_other_account_cannot_claim_or_complete | PASS |
| test_01_source_filter_before_search | PASS |
| test_02_manager_can_read_explicit_acl | PASS |
| test_03_denial_symmetric | PASS |
| test_04_role_spoof_no_effect | PASS |
| test_05_citation_allowed | PASS |
| test_06_citation_denied | PASS |
| test_07_conflict_not_silently_resolved | PASS |
| test_08_missing_pic_deadline | PASS |
| test_09_injection_quarantine | PASS |
| test_10_no_unknown_fabrication | PASS |
| test_11_tasks_complete_and_open | PASS |
| test_12_pending_does_not_execute | PASS |
| test_13_import_approved | PASS |
| test_14_receiver_cannot_import | PASS |
| test_15_accept_before_review | PASS |
| test_16_review_then_accept | PASS |
| test_17_duplicate_approval_blocked | PASS |
| test_18_stale_plan_blocked | PASS |
| test_19_revoke_hides_citation_and_brief | PASS |
| test_20_revoke_hides_historical_log | PASS |
| test_21_audit_is_user_scoped | PASS |
| test_22_manager_brief_not_shared | PASS |
| test_23_clarification_persisted | PASS |
| test_24_new_input_reopens_accepted | PASS |
| test_25_create_workspace | PASS |
| test_26_invalid_session | PASS |
| test_27_cross_workspace_access | PASS |
| test_28_http_boundary | PASS |
| test_29_open_tasks_intent | PASS |
| test_30_task_intent_no_restricted_source | PASS |
| test_31_status_intent_surfaces_conflict | PASS |
| test_32_task_intent_empty_workspace | PASS |
| test_33_oversized_body_returns_413 | PASS |
| test_forged_citation_rejected | PASS |
| test_invalid_quote_and_schema | PASS |
| test_provider_http_error | PASS |
| test_real_http_transport_to_synthetic_provider | PASS |
| test_unknown_no_provider_call | PASS |
| test_audit_no_other_user_rows | PASS |
| test_clarification_and_accepted_revision_reopens | PASS |
| test_confirmation_rollback_includes_mutation_and_audit | PASS |
| test_cross_user_workspace_and_source_not_disclosed | PASS |
| test_csrf_origin_enforced | PASS |
| test_draft_private_then_review_accept | PASS |
| test_injection_quarantined_as_data | PASS |
| test_logout_invalidates_cookie | PASS |
| test_missing_credentials_explicit_503 | PASS |
| test_model_brief_cannot_read_restricted_source | PASS |
| test_model_failure_no_fake_answer_or_brief | PASS |
| test_no_legacy_approve_endpoint_and_invalid_payload | PASS |
| test_old_accept_plan_invalid_when_new_draft_same_revision | PASS |
| test_pending_and_actor_bound_confirmation | PASS |
| test_rate_limit | PASS |
| test_receiver_mutation_denied | PASS |
| test_restart_preserves_accounts_data_and_sessions | PASS |
| test_revocation_clears_history_brief_log_model_context | PASS |
| test_revoke_during_model_call_discards_answer | PASS |
| test_revoke_during_model_call_discards_brief | PASS |
| test_role_claim_and_client_identity_ignored | PASS |
| test_session_cookie_hash_password | PASS |
| test_source_citations_and_conflicts | PASS |
| test_stale_plan_and_replay | PASS |
| test_unknown_symmetry_and_source_before_model | PASS |
| test_wrong_login_and_legacy_token_rejected | PASS |

Dataset/test resmi: belum tersedia. Percakapan dan screenshot WorkBuddy: belum diuji/direkam. Browser dan runtime produksi: lihat evidence/browser-mvp.md (MVP), evidence/browser-results.md (versi sebelumnya), dan evidence/production-smoke.json. Deteksi instruksi tersisip memakai pola terbatas dan bukan jaminan keamanan LLM. Tidak ada pengukuran waktu hemat.
