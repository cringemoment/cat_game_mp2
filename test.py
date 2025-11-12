COLLISION_FORCE = 5000  # tweakable constant

def collide_x(self, obj1, obj2):
    """Apply collision response along X using forces, not manual position snapping."""
    if not obj1.rect.colliderect(obj2.rect):
        return False

    pushback_factor = getattr(obj2, "pushback_factor", 1)

    # Determine direction and penetration
    if obj1.rect.right > obj2.rect.left and obj1.rect.left < obj2.rect.left:  # obj1 going right
        dx = obj1.rect.right - obj2.rect.left
        normal_dir = -1  # push left
    elif obj1.rect.left < obj2.rect.right and obj1.rect.right > obj2.rect.right:  # obj1 going left
        dx = obj2.rect.right - obj1.rect.left
        normal_dir = 1  # push right
    else:
        return False

    # Compute collision impulse proportional to overlap
    impulse = dx * COLLISION_FORCE

    # Apply forces in opposite directions
    obj1.forces["collision"]["x"] = normal_dir * impulse * pushback_factor
    obj2.forces["collision"]["x"] = -normal_dir * impulse * (1 - pushback_factor)

    # Optional: minor correction to prevent sinking
    obj1.rect.x += normal_dir * -dx * pushback_factor
    obj2.rect.x += normal_dir * dx * (1 - pushback_factor)

    # Trigger events
    if hasattr(obj1, "sprite_collision"):
        obj1.sprite_collision(obj2)
    if hasattr(obj2, "sprite_collision"):
        obj2.sprite_collision(obj1)

    return True


def collide_y(self, obj1, obj2):
    """Apply collision response along Y using forces."""
    if not obj1.rect.colliderect(obj2.rect):
        return False

    pushback_factor = getattr(obj2, "pushback_factor", 1)

    # Determine direction and penetration
    if obj1.rect.bottom > obj2.rect.top and obj1.rect.top < obj2.rect.top:  # obj1 falling down
        dy = obj1.rect.bottom - obj2.rect.top
        normal_dir = -1  # push up
        obj1.on_ground = True
        obj1.vely = 0
    elif obj1.rect.top < obj2.rect.bottom and obj1.rect.bottom > obj2.rect.bottom:  # obj1 going up
        dy = obj2.rect.bottom - obj1.rect.top
        normal_dir = 1  # push down
    else:
        return False

    # Compute impulse
    impulse = dy * COLLISION_FORCE

    # Apply collision forces
    obj1.forces["collision"]["y"] = normal_dir * impulse * pushback_factor
    obj2.forces["collision"]["y"] = -normal_dir * impulse * (1 - pushback_factor)

    # Position correction to avoid interpenetration
    obj1.rect.y += normal_dir * -dy * pushback_factor
    obj2.rect.y += normal_dir * dy * (1 - pushback_factor)

    if hasattr(obj1, "sprite_collision"):
        obj1.sprite_collision(obj2)
    if hasattr(obj2, "sprite_collision"):
        obj2.sprite_collision(obj1)

    return True


def handle_collisions(self, colliders, dt):
    """Apply motion, integrate forces, and resolve collisions."""
    # integrate horizontal motion from accumulated forces
    net_fx = sum(f["x"] for f in self.forces.values())
    self.velx += (net_fx / self.mass) * dt
    self.x += self.velx * dt
    self.rect.x = int(self.x)

    # resolve X collisions
    for _ in range(PHYSICS_RERUN_COUNT):
        for obj in colliders:
            if self.collide_x(self, obj):
                break
        else:
            break

    # integrate vertical motion
    net_fy = sum(f["y"] for f in self.forces.values()) + GRAVITY * self.mass
    self.vely += (net_fy / self.mass) * dt
    self.y += self.vely * dt
    self.rect.y = int(self.y)
    self.on_ground = False

    # resolve Y collisions
    for obj in colliders:
        self.collide_y(self, obj)

    # clear per-frame collision forces (so they re-accumulate next frame)
    self.forces["collision"]["x"] = 0
    self.forces["collision"]["y"] = 0
