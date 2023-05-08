#include <stdio.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int main(void) {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    luaL_dostring(L, "print('Hello, world!')");
    
    lua_close(L);
    return 0;
}
