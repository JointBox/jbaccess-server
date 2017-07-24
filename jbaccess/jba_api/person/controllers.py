from api_commons.common import ApiResponse
from django.http import HttpRequest
from jba_api import permissions
from jba_api.acls.dto import PersonAclOutDto
from jba_api.common import JbAccessController, dto_inject
from jba_api.keys.dto import KeyOutDto
from jba_api.person.dto import PersonInDto, PersonOutDto
from jba_api.roles.dto import RoleOutDto
from jba_core.service import PersonService, AclService


class PersonController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def get(self, request: HttpRequest):
        personnel = PersonService.get_all()
        person_dtos = list([PersonOutDto.from_person(p) for p in personnel])
        return ApiResponse.success(person_dtos)

    @dto_inject(PersonInDto)
    def post(self, request: HttpRequest, dto: PersonInDto):
        person = PersonService.create(dto.name)
        return ApiResponse.success(PersonOutDto.from_person(person))


class PersonRUDController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def get(self, request: HttpRequest, id: str):
        id = self.parse_int_pk(id)
        person = PersonService.get(id)
        return ApiResponse.success(PersonOutDto.from_person(person))

    @dto_inject(PersonInDto)
    def put(self, request: HttpRequest, id: str, dto: PersonInDto):
        id = self.parse_int_pk(id)
        person = PersonService.update(id, dto.name)
        return ApiResponse.success(PersonOutDto.from_person(person))

    def delete(self, request: HttpRequest, id: str):
        id = self.parse_int_pk(id)
        PersonService.delete(id)
        return ApiResponse.success()


class GetKeysController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def get(self, request: HttpRequest, id: str):
        id = self.parse_int_pk(id)
        keys = PersonService.get_keys(id)
        key_dtos = list([KeyOutDto.from_key(k) for k in keys])
        return ApiResponse.success(key_dtos)


class GetRolesController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def get(self, request: HttpRequest, id: str):
        id = self.parse_int_pk(id)
        roles = PersonService.get_roles(id)
        key_dtos = list([RoleOutDto.from_role(r) for r in roles])
        return ApiResponse.success(key_dtos)


class PersonRolesCDController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def put(self, request: HttpRequest, person_id: str, role_id: str):
        person_id = self.parse_int_pk(person_id)
        role_id = self.parse_int_pk(role_id)
        PersonService.attach_role(person_id, role_id)
        return ApiResponse.success()

    def delete(self, request: HttpRequest, person_id: str, role_id: str):
        person_id = self.parse_int_pk(person_id)
        role_id = self.parse_int_pk(role_id)
        PersonService.detach_role(person_id, role_id)
        return ApiResponse.success()


class PersonPlaceGetAclsController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def get(self, request: HttpRequest, id: str):
        id = self.parse_int_pk(id)
        acls = AclService.get_person_acls(id)
        acl_dtos = list([PersonAclOutDto.from_person_acl(a) for a in acls])
        return ApiResponse.success(acl_dtos)


class PersonAllowPlaceController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def put(self, request: HttpRequest, person_id: str, place_id: str):
        person_id = self.parse_int_pk(person_id)
        place_id = self.parse_int_pk(place_id)
        acl = AclService.person_allow_place(person_id, place_id)
        return ApiResponse.success(PersonAclOutDto.from_person_acl(acl))


class PersonDenyPlaceController(JbAccessController):
    permission_classes = [permissions.JbAccessPermission]

    def put(self, request: HttpRequest, person_id: str, place_id: str):
        person_id = self.parse_int_pk(person_id)
        place_id = self.parse_int_pk(place_id)
        acl = AclService.person_deny_place(person_id, place_id)
        return ApiResponse.success(PersonAclOutDto.from_person_acl(acl))
