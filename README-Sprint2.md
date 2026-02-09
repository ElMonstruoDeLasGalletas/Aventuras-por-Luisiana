# Sprint 2

## Requisitos del Sprint

Durante este sprint, el objetivo principal fue implementar funcionalidades relacionadas con la experiencia del usuario y la gestión de datos. Los requisitos definidos fueron:

- **Recomendaciones**: Permitir sugerencias personalizadas basadas en preferencias del usuario.  
- **Offline Sync**: Posibilidad de sincronizar datos cuando el usuario no esté conectado.  
- **Favoritos**: Permitir que el usuario marque elementos como favoritos y los gestione.

## Cambios realizados

- Se han añadido **routers/routes** con soporte completo para operaciones CRUD.  
- La carpeta `schemas` contiene contenido, pero actualmente **no está operativa**. Los esquemas que funcionan se encuentran en `app/schemas.py`.  
- Se ha modificado la funcionalidad de reviews: ahora **las reseñas se aplican a Routes** en lugar de POIs.  
- Se han implementado **recomendaciones** (`preferences`), aunque de momento solo se pueden **crear y listar**.  
- Se ha añadido la gestión de **favoritos**, permitiendo **crear, eliminar y listar** los favoritos de un usuario.
