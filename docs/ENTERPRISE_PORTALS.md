# NAMO SETU enterprise management system

## Tenant model

Every temple trust, partner company, state board and government organisation is an isolated organization. Membership binds a user to one organization with a role and permission overrides. Platform roles control cross-tenant administration; organization roles control only tenant-owned records. Every query includes tenant scope and soft-delete constraints.

## Portal catalogue

Super Admin provides executive KPIs, governance, security, global catalogue and system configuration. Domain workspaces cover temple trusts, hotels, dharamshalas, agencies, tour operators, cabs, buses, pandits, guides, restaurants, NGOs and tourism boards. Functional workspaces cover finance, support, AI operations, marketing, CMS, operations and vendor management.

## Permission model

Permissions follow `module.resource.action`, for example `bookings.refund.approve`. Default roles are permission bundles; tenant owners may create narrower custom roles. High-risk actions require recent 2FA, reason capture and immutable audit events.

| Capability | Super Admin | Regional Admin | Partner Admin | Finance | Support | Editor |
|---|---:|---:|---:|---:|---:|---:|
| Cross-tenant analytics | ✓ | Region | — | Read | — | — |
| Partner verification | ✓ | Region | — | — | — | — |
| Refund approval | ✓ | Limit | Own request | ✓ | Request | — |
| User suspension | ✓ | Region | Own staff | — | Request | — |
| Content publish | ✓ | Region | Own listing | — | — | ✓ |
| Security settings | ✓ | — | Own tenant | — | — | — |

## CRM workflow

Lead captured → identity resolution → consent recorded → assignment → qualification → itinerary/offer → follow-up task → conversion or loss reason. User, booking, support and AI interaction timelines share identifiers but sensitive conversation or health data is separately permissioned.

## Finance and settlements

The booking ledger is immutable. Payment capture creates provider and platform ledger entries. Commission, tax, refund and partner payable are derived entries. Settlement batches require maker-checker approval, reconciliation and signed exports.

## Support SLA

Priority determines response and resolution deadlines. Automation routes safety and payment incidents immediately. Breach timers continue across channel changes. Every email, chat and WhatsApp interaction is attached to one ticket timeline.

## Audit and reporting

Actor, tenant, role, action, target, before/after hash, IP, device, request ID and reason are recorded. Reports are generated asynchronously from read replicas and delivered through expiring signed URLs. Exports inherit the viewer's row and field permissions.
