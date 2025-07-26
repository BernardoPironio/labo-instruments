# labo-instruments

**Control de instrumentos de laboratorio con PyVISA**

Este paquete reúne clases en Python para el control de instrumentos físicos de laboratorio, tales como generadores de funciones, osciloscopios y multiplexores. Las clases fueron originalmente compartidas por docentes de la Facultad de Ciencias Exactas y Naturales de la Universidad de Buenos Aires (UBA), y fueron reorganizadas en forma de paquete instalable para facilitar su uso, mantenimiento y extensión.

---

## 📦 Contenido del paquete

Este paquete incluye, actualmente, controladores para los siguientes instrumentos:

- **Agilent 34970A** — Multiplexor Agilent 34970A
- **Tektronix TDS1002B** — Osciloscopio Tektronix TDS1002B
- **SR830** — LOCKIN Stanford Research SR830

Cada clase permite interactuar con el equipo correspondiente mediante comandos SCPI a través de la librería [PyVISA](https://pyvisa.readthedocs.io/).

---

## ✍️ Autoría y agradecimientos

Las versiones originales de estos scripts fueron desarrolladas por docentes del Departamento de Física (UBA Exactas). Este repositorio fue reorganizado y empaquetado por un estudiante, con el objetivo de facilitar su instalación, uso y modificación.

---

## 🚀 Instalación

Una vez subido a PyPI:

```bash
pip install labo-instruments
