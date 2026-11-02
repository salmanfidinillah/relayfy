# Hasil pengujian aktual

Synthetic deterministic core + local HTTP; NOT actual WorkBuddy/LLM or official tests

Run UTC: 2026-11-01T15:17:30.469301+00:00

28/28 lulus.

| Kasus | Hasil |
|---|---|
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

Dataset/test resmi: belum tersedia. Percakapan dan screenshot WorkBuddy: belum diuji/direkam. Deteksi instruksi tersisip memakai pola terbatas dan bukan jaminan keamanan LLM. Tidak ada pengukuran waktu hemat.
