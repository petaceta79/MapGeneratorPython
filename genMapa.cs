using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static Random random = new Random();

    // Generar raiz vacia
    static List<List<int>> GenerarArrayMapa(int distancia)
    {
        var mapa = new List<List<int>>();
        for (int i = 0; i <= distancia; i++)
        {
            mapa.Add(new List<int>(new int[distancia + 1]));
        }
        return mapa;
    }

    // Funciones para obtener info del mapa
    static void VerMapaCMD(List<List<int>> mapa)
    {
        foreach (var fila in mapa)
        {
            Console.WriteLine(string.Join(" ", fila));
        }
    }

    static int ContadorSalas(List<List<int>> mapa, int? valores = null)
    {
        int numeroSalas = 0;
        foreach (var fila in mapa)
        {
            foreach (var celda in fila)
            {
                if (valores == null)
                {
                    if (celda != 0)
                    {
                        numeroSalas++;
                    }
                }
                else
                {
                    if (celda == valores)
                    {
                        numeroSalas++;
                    }
                }
            }
        }
        return numeroSalas;
    }

    static List<int[]> PosicionDeCasillas(List<List<int>> mapa)
    {
        var casillasPosicion = new List<int[]>();
        for (int i = 0; i < mapa.Count; i++)
        {
            for (int j = 0; j < mapa[i].Count; j++)
            {
                if (mapa[i][j] != 0)
                {
                    casillasPosicion.Add(new int[] { i, j });
                }
            }
        }
        return casillasPosicion;
    }

    static bool EstaRodeadaSiONo(List<List<int>> mapa, int[] posicion, List<int> valores = null)
    {
        if (valores == null) valores = new List<int> { 0 };
        int x = posicion[0], y = posicion[1];
        int max_x = mapa.Count - 1, max_y = mapa[0].Count - 1;
        if (x == 0 || x == max_x || y == 0 || y == max_y) return false;

        var neighbors = new List<int[]> {
            new int[] { x + 1, y }, new int[] { x - 1, y },
            new int[] { x, y + 1 }, new int[] { x, y - 1 },
            new int[] { x + 1, y + 1 }, new int[] { x + 1, y - 1 },
            new int[] { x - 1, y + 1 }, new int[] { x - 1, y - 1 }
        };

        foreach (var neighbor in neighbors)
        {
            int nx = neighbor[0], ny = neighbor[1];
            if (valores.Contains(mapa[nx][ny])) return false;
        }
        return true;
    }

    static bool EstaTocandoHabitacion(List<List<int>> mapa, int[] posicion)
    {
        int x = posicion[0], y = posicion[1];
        int max_x = mapa.Count - 1, max_y = mapa[0].Count - 1;
        if (x == 0 || x == max_x || y == 0 || y == max_y) return false;

        var neighbors = new List<int[]> {
            new int[] { x + 1, y }, new int[] { x - 1, y },
            new int[] { x, y + 1 }, new int[] { x, y - 1 }
        };

        foreach (var neighbor in neighbors)
        {
            int nx = neighbor[0], ny = neighbor[1];
            if (mapa[nx][ny] != 0) return true;
        }
        return false;
    }

    static List<int[]> PosicionDePosiblesCasillasEspeciales(List<List<int>> mapa, List<int> valores)
    {
        var casillasPosicion = new List<int[]>();
        for (int i = 0; i < mapa.Count; i++)
        {
            for (int j = 0; j < mapa[i].Count; j++)
            {
                if (EstaRodeadaSiONo(mapa, new int[] { i, j }, valores) && mapa[i][j] == 0 && EstaTocandoHabitacion(mapa, new int[] { i, j }))
                {
                    casillasPosicion.Add(new int[] { i, j });
                }
            }
        }
        return casillasPosicion;
    }

    static bool EliminarRodeadas(List<List<int>> mapa, int[] posicion, double porcentageEliminarRodeadas, List<int> casillasEspeciales)
    {
        if (EstaRodeadaSiONo(mapa, posicion) && random.NextDouble() <= porcentageEliminarRodeadas && !casillasEspeciales.Contains(mapa[posicion[0]][posicion[1]]))
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    static List<List<int>> AmpliarMapa(List<List<int>> mapa, int numeroCasillas, List<int> tiposDeHabitaciones, double porcentageEliminarRodeadas, List<int> casillasEspeciales, List<int> numeroEspeciales)
    {
        if (numeroCasillas + 1 <= (mapa.Count * mapa.Count))
        {
            while (ContadorSalas(mapa) < numeroCasillas + 1)
            {
                var posicionACambiar = PosicionDeCasillas(mapa)[random.Next(PosicionDeCasillas(mapa).Count)];
                int direccion = random.Next(1, 5);
                if (direccion == 1 && posicionACambiar[0] != 0 && mapa[posicionACambiar[0] - 1][posicionACambiar[1]] == 0)
                {
                    mapa[posicionACambiar[0] - 1][posicionACambiar[1]] = tiposDeHabitaciones[random.Next(tiposDeHabitaciones.Count)];
                }
                if (direccion == 2 && posicionACambiar[1] != mapa[0].Count - 1 && mapa[posicionACambiar[0]][posicionACambiar[1] + 1] == 0)
                {
                    mapa[posicionACambiar[0]][posicionACambiar[1] + 1] = tiposDeHabitaciones[random.Next(tiposDeHabitaciones.Count)];
                }
                if (direccion == 3 && posicionACambiar[0] != mapa.Count - 1 && mapa[posicionACambiar[0] + 1][posicionACambiar[1]] == 0)
                {
                    mapa[posicionACambiar[0] + 1][posicionACambiar[1]] = tiposDeHabitaciones[random.Next(tiposDeHabitaciones.Count)];
                }
                if (direccion == 4 && posicionACambiar[1] != 0 && mapa[posicionACambiar[0]][posicionACambiar[1] - 1] == 0)
                {
                    mapa[posicionACambiar[0]][posicionACambiar[1] - 1] = tiposDeHabitaciones[random.Next(tiposDeHabitaciones.Count)];
                }
            }
            foreach (var e in PosicionDeCasillas(mapa))
            {
                if (EliminarRodeadas(mapa, e, porcentageEliminarRodeadas, casillasEspeciales))
                {
                    mapa[e[0]][e[1]] = 0;
                }
            }

            for (int cas = 0; cas < casillasEspeciales.Count; cas++)
            {
                while (ContadorSalas(mapa, casillasEspeciales[cas]) < numeroEspeciales[cas])
                {
                    var posiblePosiciones = PosicionDePosiblesCasillasEspeciales(mapa, casillasEspeciales);
                    var posicionElegida = posiblePosiciones[random.Next(posiblePosiciones.Count)];
                    mapa[posicionElegida[0]][posicionElegida[1]] = casillasEspeciales[cas];
                }
            }
        }
        return mapa;
    }

    static List<List<int>> CrearMapa(int tamanoDelMapa = 15, int numeroDeHabitaciones = 75, List<int> tiposDeHabitaciones = null, double porcentageEliminarRodeadas = 0.45, List<int> casillasEspeciales = null, List<int> numeroEspeciales = null)
    {
        if (tiposDeHabitaciones == null) tiposDeHabitaciones = new List<int> { 10, 11, 12, 13, 14, 15 };
        if (casillasEspeciales == null) casillasEspeciales = new List<int> { 1, 2, 3, 4 };
        if (numeroEspeciales == null) numeroEspeciales = new List<int> { 1, 1, 1, 1 };

        var mapa = GenerarArrayMapa(tamanoDelMapa - 1);
        mapa[mapa.Count / 2][mapa[0].Count / 2] = 1;

        mapa = AmpliarMapa(mapa, numeroDeHabitaciones - 1, tiposDeHabitaciones, porcentageEliminarRodeadas, casillasEspeciales, numeroEspeciales);

        return mapa;
    }

    static void Main(string[] args)
    {
        var mapa = CrearMapa(15, 50, new List<int> { 10, 11, 12, 13, 14, 15 }, 0.5, new List<int> { 1, 2, 3 }, new List<int> { 1, 1, 1 });
        VerMapaCMD(mapa);
        Console.WriteLine("-------");
        Console.WriteLine(mapa[7][7]);
    }
}


