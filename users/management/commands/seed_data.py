from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from users.models import PermissionAtom, Profile, ProfilePermission
from catalog.models import Category, Product
from orders.models import Subscription

class Command(BaseCommand):
    help = 'Semilla inicial de permisos, perfiles, categorías y catálogo de productos demostrativos.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando la carga de datos de prueba...")

        # ----------------------------------------------------
        # 1. Crear Permisos Atómicos
        # ----------------------------------------------------
        permissions_data = [
            # Módulo Seguridad / Administración
            ('users:ver:todos', 'users', 'Ver listado de todos los usuarios'),
            ('users:modificar_perfiles', 'users', 'Asignar o revocar perfiles a usuarios'),
            ('profiles:gestionar', 'users', 'Configurar permisos de perfiles dinámicos'),
            ('audit:ver', 'users', 'Ver logs de auditoría de seguridad'),
            
            # Módulo Catálogo
            ('catalog:crear', 'catalog', 'Crear y modificar productos del catálogo'),
            
            # Módulo Pedidos
            ('orders:ver_todos', 'orders', 'Ver pedidos de todos los usuarios'),
            ('orders:gestionar_estado', 'orders', 'Actualizar el estado de los pedidos'),
            
            # Módulo Tutor Visual IA
            ('tutor:acceso', 'tutor', 'Acceso para consultar al Tutor Visual IA'),
            
            # Módulo Marketing / Banners y Promociones
            ('banners:ver:todos', 'banners', 'Ver banners publicitarios'),
            ('banners:crear:todos', 'banners', 'Crear nuevos banners publicitarios'),
            ('banners:eliminar:todos', 'banners', 'Eliminar banners publicitarios'),
            ('promociones:gestionar', 'promociones', 'Crear cupones y descuentos'),
        ]

        permission_atoms = {}
        for code, module, desc in permissions_data:
            atom, created = PermissionAtom.objects.get_or_create(
                code=code,
                defaults={'module': module, 'description': desc}
            )
            permission_atoms[code] = atom
            if created:
                self.stdout.write(f"Permiso creado: {code}")

        # ----------------------------------------------------
        # 2. Crear Perfiles por Defecto
        # ----------------------------------------------------
        # Perfil 1: Comprar en la tienda (Cliente base)
        client_profile, _ = Profile.objects.get_or_create(
            name="Comprar en la tienda",
            defaults={'description': 'Perfil base para compras ordinarias en la tienda.'}
        )

        # Perfil 2: Tutor Visual IA (Premium)
        premium_profile, _ = Profile.objects.get_or_create(
            name="Tutor Visual IA",
            defaults={'description': 'Habilita el uso del Tutor Visual con Inteligencia Artificial.'}
        )
        # Asignar permiso tutor
        ProfilePermission.objects.get_or_create(
            profile=premium_profile,
            permission=permission_atoms['tutor:acceso'],
            defaults={'scope': 'propios'}
        )

        # Perfil 3: Pasante de Marketing (Ejemplo con vencimiento en requisitos)
        marketing_profile, _ = Profile.objects.get_or_create(
            name="Pasante de Marketing",
            defaults={'description': 'Gestión de banners y promociones.'}
        )
        # Asignar permisos banners (ver y crear, sin eliminar)
        ProfilePermission.objects.get_or_create(
            profile=marketing_profile,
            permission=permission_atoms['banners:ver:todos'],
            defaults={'scope': 'todos'}
        )
        ProfilePermission.objects.get_or_create(
            profile=marketing_profile,
            permission=permission_atoms['banners:crear:todos'],
            defaults={'scope': 'todos'}
        )

        # Perfil 4: Vendedor / Proveedor
        vendor_profile, _ = Profile.objects.get_or_create(
            name="Vendedor/Proveedor",
            defaults={'description': 'Administración del catálogo y procesamiento de pedidos.'}
        )
        ProfilePermission.objects.get_or_create(
            profile=vendor_profile,
            permission=permission_atoms['catalog:crear'],
            defaults={'scope': 'propios'}
        )
        ProfilePermission.objects.get_or_create(
            profile=vendor_profile,
            permission=permission_atoms['orders:ver_todos'],
            defaults={'scope': 'todos'}
        )
        ProfilePermission.objects.get_or_create(
            profile=vendor_profile,
            permission=permission_atoms['orders:gestionar_estado'],
            defaults={'scope': 'todos'}
        )

        # Perfil 5: Administrador General
        admin_profile, _ = Profile.objects.get_or_create(
            name="Administrador del Sistema",
            defaults={'description': 'Acceso total a la configuración y auditoría.'}
        )
        for code, atom in permission_atoms.items():
            ProfilePermission.objects.get_or_create(
                profile=admin_profile,
                permission=atom,
                defaults={'scope': 'todos'}
            )

        self.stdout.write("Perfiles y permisos configurados con éxito.")

        # ----------------------------------------------------
        # 3. Crear Categorías
        # ----------------------------------------------------
        categories_data = [
            ("Obra Gruesa", ["Cementos y Cales", "Ladrillos y Bloques", "Hierros y Mallas"]),
            ("Terminaciones", ["Adhesivos y Pastinas", "Yesos y Placas de Yeso", "Pinturas e Impermeabilizantes"]),
        ]

        category_objs = {}
        for parent_name, subcategories in categories_data:
            parent_cat, _ = Category.objects.get_or_create(
                name=parent_name,
                defaults={'slug': slugify(parent_name)}
            )
            category_objs[parent_name] = parent_cat
            for sub_name in subcategories:
                sub_cat, _ = Category.objects.get_or_create(
                    name=sub_name,
                    defaults={'slug': slugify(sub_name), 'parent': parent_cat}
                )
                category_objs[sub_name] = sub_cat

        self.stdout.write("Categorías creadas.")

        # ----------------------------------------------------
        # 4. Crear Catálogo de 20 Productos Demostrativos (RF 2)
        # ----------------------------------------------------
        products_data = [
            # Cementos y Cales
            ("Cem-001", "Cemento Portland Normal Loma Negra 50kg", "Cemento de alta resistencia para estructuras de hormigón y albañilería general.", 12500.00, 150, 50.0, "Cementos y Cales"),
            ("Cem-002", "Cemento Portland Avellaneda 50kg", "Cemento de fraguado rápido y alta resistencia inicial, óptimo para losas.", 12300.00, 100, 50.0, "Cementos y Cales"),
            ("Cem-003", "Cal Hidratada Loma Negra 25kg", "Cal hidratada aérea de alta plasticidad para mezcla de revoques y contrapisos.", 5400.00, 200, 25.0, "Cementos y Cales"),
            
            # Ladrillos y Bloques
            ("Lad-001", "Ladrillo Hueco 12x18x33 (Por unidad)", "Ladrillo cerámico hueco de 6 tubos para muros portantes y divisiones.", 480.00, 2500, 4.2, "Ladrillos y Bloques"),
            ("Lad-002", "Ladrillo Hueco 18x18x33 (Por unidad)", "Ladrillo hueco de 9 tubos ideal para paredes exteriores y cerramientos térmicos.", 650.00, 1800, 5.8, "Ladrillos y Bloques"),
            ("Lad-003", "Ladrillo Común de Campo (Por 1000 u)", "Ladrillo macizo tradicional para hornos, paredes a la vista y cimientos.", 145000.00, 15, 2000.0, "Ladrillos y Bloques"),
            ("Lad-004", "Bloque de Hormigón 19x19x39 (Por unidad)", "Bloque de hormigón prensado para construcción modular de alta velocidad.", 980.00, 1200, 14.0, "Ladrillos y Bloques"),

            # Hierros y Mallas
            ("Hie-001", "Hierro Nervado Aluar 8mm (Barra 12m)", "Barra de acero nervado grado 420 para armaduras de hormigón armado.", 10800.00, 80, 4.74, "Hierros y Mallas"),
            ("Hie-002", "Hierro Nervado Aluar 10mm (Barra 12m)", "Barra de acero nervado grado 420 utilizada en vigas y columnas principales.", 16800.00, 60, 7.4, "Hierros y Mallas"),
            ("Hie-003", "Hierro Nervado Aluar 12mm (Barra 12m)", "Barra de acero nervado estructural de alta exigencia.", 24100.00, 40, 10.65, "Hierros y Mallas"),
            ("Hie-004", "Malla Sima C-15 15x15 (Paño 2.4x6m)", "Malla electrosoldada de alambre nervado para refuerzo de contrapisos y plateas.", 38500.00, 30, 22.0, "Hierros y Mallas"),

            # Adhesivos y Pastinas
            ("Adh-001", "Pegamento Impermeable Weber Col 25kg", "Mezcla adhesiva impermeable para la colocación de cerámicas en interiores y exteriores.", 8700.00, 90, 25.0, "Adhesivos y Pastinas"),
            ("Adh-002", "Adhesivo Weber Porcelanato Flex 25kg", "Pegamento flexible de alta tecnología para porcelanatos de gran formato.", 17500.00, 75, 25.0, "Adhesivos y Pastinas"),
            ("Adh-003", "Pastina Weber Classic 2kg (Gris)", "Mezcla cementicia para relleno de juntas de 1 a 4 mm en revestimientos.", 2900.00, 120, 2.0, "Adhesivos y Pastinas"),

            # Yesos y Placas
            ("Yes-001", "Placa de Yeso Durlock Estándar 12.5mm", "Placa de yeso estándar de 1.20 x 2.40 metros para tabiques y cielorrasos.", 14800.00, 85, 21.0, "Yesos y Placas de Yeso"),
            ("Yes-002", "Placa de Yeso Durlock Verde (Antihumedad)", "Placa de yeso impregnada para zonas húmedas como baños y cocinas.", 22300.00, 50, 22.0, "Yesos y Placas de Yeso"),
            ("Yes-003", "Yeso Manual Tuyango 40kg", "Yeso tradicional de fraguado lento para enlucidos y revoques interiores de alta calidad.", 9500.00, 110, 40.0, "Yesos y Placas de Yeso"),

            # Pinturas e Impermeabilizantes
            ("Pin-001", "Pintura Látex Interior Alba Mate 20L", "Pintura al agua de alto poder cubritivo y lavable para ambientes interiores.", 89000.00, 25, 28.0, "Pinturas e Impermeabilizantes"),
            ("Pin-002", "Membrana Líquida Weber Tech 20kg", "Impermeabilizante acrílico elastomérico con poliuretano para techos y terrazas transitables.", 124000.00, 30, 20.0, "Pinturas e Impermeabilizantes"),
            ("Pin-003", "Fijador Sellador Alba Concentrado 4L", "Acondicionador de superficies para homogeneizar la absorción antes de pintar.", 15200.00, 50, 4.2, "Pinturas e Impermeabilizantes"),
        ]

        for sku, name, desc, price, stock, weight, cat_name in products_data:
            cat = category_objs.get(cat_name)
            prod, created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': desc,
                    'price': price,
                    'stock': stock,
                    'weight_kg': weight,
                    'category': cat,
                    'image_url': f"https://via.placeholder.com/300?text={sku}"
                }
            )
            if created:
                self.stdout.write(f"Producto creado: {name}")

        # ----------------------------------------------------
        # 5. Crear Superusuario de Administración
        # ----------------------------------------------------
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                email="admin@construccion.com",
                password="adminpassword"
            )
            # Asignar perfil de Administrador del Sistema
            UserProfileAssignment.objects.create(
                user=admin_user,
                profile=admin_profile,
                assigned_by=None
            )
            self.stdout.write("Superusuario 'admin' creado (Clave: adminpassword). Perfil Administrador asignado.")

        self.stdout.write("La carga de datos semilla ha finalizado con éxito.")
