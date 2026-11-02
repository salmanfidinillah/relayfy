# Hasil pengujian aktual

Synthetic deterministic core + local HTTP; NOT actual WorkBuddy/LLM or official tests

Run UTC: 2026-11-02T03:42:31.658290+00:00

32/32 lulus.

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
| test_29_open_tasks_intent | PASS |
| test_30_task_intent_no_restricted_source | PASS |
| test_31_status_intent_surfaces_conflict | PASS |
| test_32_task_intent_empty_workspace | PASS |

## Lapisan bridge (HTTP client nyata)

Real bridge.py -> HTTP -> local service, synthetic demo data. NOT a WorkBuddy conversation and NOT official committee tests.

Run UTC: 2026-11-02T03:42:28.818378+00:00

7/7 lulus.

| Kasus | Hasil | Catatan |
|---|---|---|
| W01 | PASS | decision=evidence; chat:2 quoted; mentions foto produk |
| W02 | PASS | doc:2 and chat:1 both quoted; conflict on peluncuran reported |
| W03 | PASS | decision=tasks; tasks listed; missing pic and deadline; no invented values |
| W04 | PASS | decision=unknown; response byte-identical to a non-existent object; no secret metadata |
| W05 | PASS | decision=unknown; exact UNKNOWN message; no evidence |
| W06 | PASS | quarantined line never returned; no password text; no side effect |
| W10-struct | PASS | bridge exposes no approve operation; approval only via operator terminal |

Belum dijalankan: W07, W08, W09, W10 (lihat WORKBUDDY_CASES.md).

## Belum diuji

Dataset/test resmi panitia: belum tersedia. Percakapan dan screenshot WorkBuddy: belum dijalankan. Deteksi instruksi tersisip memakai pola terbatas dan bukan jaminan keamanan LLM. Tidak ada pengukuran waktu hemat.
